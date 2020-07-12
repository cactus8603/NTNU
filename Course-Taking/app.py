from datetime import datetime
from pytz import timezone
import requests
import time
import threading
import logging

from mongo import *
from mongo import engine


TIMEZONE_STRING = 'Asia/Taipei'
MAIN_THREAD_ALIVE_LOG = 10800 # 3 hours
TAKE_THREAD_ALIVE_LOG = 10800 # 3 hours
UPDATE_INTERVAL = 3
PREPARE_REST_TIME = 0.5
NIGHT_SLEEP_TIME = 30


def take(serial_no):

    logging.info('start.')

    start_time = datetime.now().timestamp()
    now_time = datetime.now().timestamp()

    tc = TakingCourse(serial_no)
    switch = Boolean('Course taking switch')
    packet_interval = Number('Packet interval')
    user = None

    status = 'SLEEPING'

    while tc.obj.is_performing:

        today_prepare_time = datetime.now().replace(hour=0, minute=59, second=30) # , tzinfo=tw)
        today_start_time = datetime.now().replace(hour=1, minute=00, second=00) # , tzinfo=tw)
        today_end_time = datetime.now().replace(hour=16, minute=00, second=00) # , tzinfo=tw)
        # logging.debug('now: %s / today start time: %s', str(datetime.now()), str(today_start_time))

        if datetime.now() > today_start_time and datetime.now() < today_end_time:

            status = 'RUNNING'
            
            if not switch.obj.boolean:
                time.sleep(10)

            else:
                for r in tc.obj.request_list:
                    time.sleep(packet_interval.obj.number)
                    if user is None:
                        user = User(student_id = r.user.student_id,
                                    password = r.user.password)
                        user.ntnu_login()
                        user.switch_to_add_course_page()
                        logging.info('[LOGIN] user %s (%s)', user.obj.name, user.student_id)
                    try:
                        result = user.take_course(serial_no, r.domain)
                        if result['success']:
                            tc.remove_user(user)
                            user.stop_taking_course(serial_no, 'success')
                            logging.info('[SUCCESS] by user %s (%s)', user.obj.name, user.student_id)
                            user = None
                            break
                        else:
                            if result['msg'] == '重複登記,加選失敗':
                                tc.remove_user(user)
                                user.stop_taking_course(serial_no, 'repeated')
                                logging.info('[REPEATED] by user %s (%s)', user.obj.name, user.student_id)
                                user = None
                                break
                            elif result['msg'] == '該課程與其他課程衝堂,加選失敗':
                                tc.remove_user(user)
                                user.stop_taking_course(serial_no, 'conflict')
                                logging.info('[CONFLICT] by user %s (%s)', user.obj.name, user.student_id)
                                user = None
                                break
                            elif result['msg'] == '額滿,失敗':
                                warn = result['msg']
                                logging.info('[FULL] user %s (%s): %s', user.obj.name, user.student_id, warn)
                                if user.obj != tc.obj.request_list[0].user:
                                    user = None
                                    break
                            else:
                                warn = result['msg']
                                # 課程衝堂, 通識領域錯誤, ...
                                logging.warning('[FAILED] user %s (%s): %s', user.obj.name, user.student_id, warn)
                                if len(tc.obj.request_list) > 1:
                                    user = None
                    except Exception as ex:
                        logging.error('[ERROR] user %s (%s): %s', user.obj.name, user.student_id, ex)
                        user = None
                        break

        elif datetime.now() > today_prepare_time and datetime.now() < today_start_time:
            # logging.info('preparing...')
            status = 'PREPARING'
            time.sleep(PREPARE_REST_TIME)

        else:
            # logging.info('sleeping...')
            status = 'SLEEPING'
            time.sleep(NIGHT_SLEEP_TIME)
        
        tc.obj.reload()
        switch.obj.reload()
        packet_interval.obj.reload()

        if not tc.obj.is_performing:
            break

        if datetime.now().timestamp() - now_time >= TAKE_THREAD_ALIVE_LOG:
            now_time = datetime.now().timestamp()
            logging.info(f'[ALIVE] status: {status}.')

    logging.info('[END]')


def set_threads():

    logging.info('[START] Control center')

    start_time = datetime.now().timestamp()
    now_time = datetime.now().timestamp()

    old_taking_courses = []
    while True:
        new_taking_courses = engine.TakingCourse.objects

        for ntc in new_taking_courses:
            if ntc not in old_taking_courses and ntc.is_performing:
                threading.Thread(target=take, name=ntc.serial_no, args=(ntc.serial_no, ), daemon=True).start()
                # logging.info('TakingCourse %s should start', ntc.serial_no)
        
        for otc in old_taking_courses:
            if not otc.is_performing and engine.TakingCourse.objects.get(serial_no=otc.serial_no).is_performing:
                threading.Thread(target=take, name=otc.serial_no, args=(otc.serial_no, ), daemon=True).start()
                # logging.info('TakingCourse %s should start', otc.serial_no)

        old_taking_courses = new_taking_courses

        time.sleep(UPDATE_INTERVAL)
        if datetime.now().timestamp() - now_time >= MAIN_THREAD_ALIVE_LOG:
            now_time = datetime.now().timestamp()
            logging.info('[ALIVE] Control center')
    
    logging.info('[END] Control center')


def timetz(*args):
    return datetime.now(timezone(TIMEZONE_STRING)).timetuple()


def main():
    # log_filename = datetime.now().strftime('%Y-%m-%d_%H_%M_%S.log')
    log_filename = 'robot.log'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s | %(funcName)-15s | %(threadName)-10s | %(message)s',
                        datefmt='%Y/%m/%d - %I:%M:%S %p',
                        handlers=[logging.FileHandler(log_filename, 'a+', 'utf-8')])
    logging.Formatter.converter = timetz

    set_threads()

main()