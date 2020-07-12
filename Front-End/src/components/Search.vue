<template>
  <v-container fluid
    class="fill-height"
  >
    <!-- 查詢警告遮罩 -->
    <v-overlay absolute :value="searchAlert">
      <v-card outlined light>
        <v-toolbar dark flat dense
          color="primary"
        >
          <v-toolbar-title centered>警告</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <div class="subtitle-1 text--primary">
            若您現在正使用手機瀏覽本網頁，<br>
            <b>請勿</b> 直接查詢所有課程！<br>
            因為本學期共有 <b>4056</b> 堂課，<br>
            資料量龐大，容易導致手機當機。
          </div>
        </v-card-text>
        <v-card-actions>
          <v-row justify="center"><v-col cols="auto" class="pa-0">
            <v-btn @click="$emit('searchAlertConfirm')">我知道了</v-btn>
          </v-col></v-row>
        </v-card-actions>
      </v-card>
    </v-overlay>

    <!-- 查詢中遮罩 -->
    <v-overlay absolute :value="searching">
      <v-row justify="center">
        <v-col cols="auto">
          <v-progress-circular indeterminate size="64"/>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="auto" class="headline">查詢中...</v-col>
      </v-row>
    </v-overlay>

    <!-- Take Confirm 遮罩 -->
    <v-overlay absolute v-if="takeConfirm">
      <v-card outlined light v-if="targetCourse.deptCode == '9UAA' || targetCourse.deptCode == '9UAB'">
        <v-toolbar dark flat dense
          color="primary"
        >
          <v-toolbar-title centered>訊息</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <div class="subtitle-1 text--primary">
            很抱歉，台大和台科大尚未開放搶課功能。<br>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-row justify="space-around">
            <v-col cols="auto" class="pa-0"><v-btn @click="takeConfirm=false">我知道了</v-btn></v-col>
          </v-row>
        </v-card-actions>
      </v-card>
      <v-card outlined light v-else>
        <v-toolbar dark flat dense
          color="primary"
        >
          <v-toolbar-title centered>確認</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <div class="subtitle-1 text--primary">
            請問您是否確定這是您想要的課程：<br>
            代碼：<b>{{ targetCourse.serialNo }}</b><br>
            名稱：<b>{{ targetCourse.name }}</b><br>
            時間：<b>{{ targetCourse.timeInfo }}</b>

            <v-select dense hide-details single-line outlined filled clearable
              v-if="targetCourse.deptCode == 'GU'"
              v-model="targetDomain"
              label="請選擇通識領域"
              :items="domains"
            />
          </div>
        </v-card-text>
        <v-card-actions>
          <v-row justify="space-around">
            <v-col cols="auto" class="pa-0"><v-btn @click="addTake">是</v-btn></v-col>
            <v-col cols="auto" class="pa-0"><v-btn @click="takeConfirm=false">否</v-btn></v-col>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-overlay>

    <!-- take result 遮罩 -->
    <v-overlay absolute :value="takeResult">
      <v-row v-if="takeResult == 1" justify="center">
        <v-col cols="auto">
          <v-progress-circular indeterminate size="64"/>
        </v-col>
      </v-row>
      <v-row v-if="takeResult == 1" justify="center">
        <v-col cols="auto" class="headline">正在登記...</v-col>
      </v-row>
      <v-card outlined light
        v-if="takeResult == 2 || takeResult == 3"
        width="250px"
      >
        <v-toolbar dark flat dense color="primary">
          <v-toolbar-title centered>訊息</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <div v-if="takeResult == 2" class="subtitle-1 text--primary">
            <b>成功。</b>
          </div>
          <div v-else class="subtitle-1 text--primary">
            <b>失敗。</b><br>
            這可能是 bug 導致的，<br>
            也可能是因為非法操作。<br>
            請將詳細情況告知開發者～
          </div>
        </v-card-text>
        <v-card-actions>
          <v-row justify="center"><v-col cols="auto" class="pa-0">
            <v-btn @click="$emit('closeTakeResult')">我知道了</v-btn>
          </v-col></v-row>
        </v-card-actions>
      </v-card>
    </v-overlay>

    <!-- Domain Null Alert -->
    <v-snackbar top
      class="mt-8 pt-8"
      v-model="DomainNullAlert"
      color="red"
      :timeout="3000"
    >
      請選擇通識領域。
      <v-btn dark text
        @click="DomainNullAlert = false"
      >
        好的
      </v-btn>
    </v-snackbar>

    <v-card outlined
      id="v-card-1"
      class="flex-grow-1"
    >
      <v-toolbar dark flat dense
        color="primary"
      >
        <v-toolbar-title>查詢課程</v-toolbar-title>
      </v-toolbar>
      
      <!-- 查詢表格 -->
      <v-row no-gutters
        align-content="start"
      >
        <!-- 課程代碼 -->
        <v-col
          cols="4"
          xs="4"
          sm="2"
        >
          <v-card outlined tile
            class="pa-1"
          >
            <v-text-field dense hide-details single-line outlined filled
              v-model="serialNoInput"
              label="課程代碼"
              :rules="rules"
            />
          </v-card>
        </v-col>

        <!-- 課程名稱 -->
        <v-col
          cols="8"
          xs="8"
          sm="10"
        >
          <v-card outlined tile
            class="pa-1"
          >
            <v-text-field dense hide-details single-line outlined filled
              v-model="nameInput"
              label="課程名稱"
            />
          </v-card>
        </v-col>

        <!-- 科系選擇器 -->
        <v-col
          cols="6"
          sm="4"
        >
          <v-card outlined tile
            class="pa-1"
          >
            <v-select dense hide-details single-line outlined filled clearable
              v-model="departmentSelector"
              label="科系"
              :items="departments"
            />
          </v-card>
        </v-col>

        <!-- 通識領域選擇器 -->
        <v-col
          cols="6"
          sm="4"
        >
          <v-card outlined tile
            class="pa-1"
          >
            <v-select dense hide-details single-line outlined clearable
              v-model="domainSelector"
              label="通識領域"
              :items="domains"
              :filled="departmentSelector == 'GU'"
              :disabled="departmentSelector != 'GU'"
            ></v-select>
          </v-card>
        </v-col>
        
        <!-- 時間選擇器 -->
        <v-col>
          <v-card outlined tile
            class="ma-1"
          >
            <v-menu
              :close-on-content-click="false"
            >
              <template
                v-slot:activator="{ on }"
              >
                <v-btn text block tile
                  v-on="on"
                >
                  時間 (本功能尚未開發完成)
                </v-btn>
              </template>

              <v-card
                class="pa-3"
              >
                <v-row dense
                  class="pa-0"
                  justify="center"
                >
                  <v-col
                    cols="auto"
                    class="pl-2 pr-3 pt-0 pb-0"
                  >
                    <v-row dense
                      class="pa-0"
                      v-for="(time, n) in periods"
                      justify="center"
                      align="end"
                      :key="n"
                    >
                      {{ time }}
                    </v-row>
                  </v-col>
                  <v-col
                    cols="auto"
                    class="pa-0"
                    v-for="(day, m) in times"
                    :key="m"
                  >
                    {{ weeks[m] }}
                    <v-row dense
                      class="pa-0"
                      v-for="(time, n) in day"
                      justify="center"
                      align="end"
                      :key="n"
                    >
                      <v-checkbox dense hide-details
                        class="pa-0 ma-0"
                        v-model="times[m][n]"
                      />
                    </v-row>
                  </v-col>
                </v-row>
              </v-card>
            </v-menu>
          </v-card>
        </v-col>

        <!-- 查詢按鈕 -->
        <v-col
          cols="auto"
        >
          <v-card outlined tile>
            <v-btn dark depressed top
              height="48px"
              color="indigo"
              @click="searchCourses"
            >
              <v-icon x-large>mdi-magnify</v-icon>
            </v-btn>
          </v-card>
        </v-col>
      </v-row>

      <!-- 查詢結果表格 -->
      <v-card outlined tile>
        <v-data-table show-expand fixed-header
          :mobile-breakpoint="300"
          :no-data-text="noDataText"
          :headers="headers"
          :items="courses"
          :items-per-page="50"
          :footer-props="{
            itemsPerPageOptions: [ 10, 50, 100, 500, -1 ],
            itemsPerPageAllText: '全部',
            itemsPerPageText: '每頁數量',
            showCurrentPage: true
          }"
          height="53vh"
          item-key="serialNo"
          class="elevation-1"
        >
        <!-- height="60vh(phone) / 61vh(ubuntu chrome) /
                     70vh(ubuntu chrome all-screen)" -->
          <template v-if="isLogin" v-slot:expanded-item="{ headers, item }">
            <td :colspan="headers.length" class="pa-0">
              <v-card tile flat color="rgb(0, 0, 0, 0)" class="pl-5 pr-5 pt-0 pb-0">
                <v-row align="center">
                  <v-col cols="8">
                    <b>老師：</b> {{ item.teacher }}<br>
                    <b>備註：</b> {{ item.vComment != '' ? item.vComment : '無' }}<br>
                    <b>限制：</b> {{ item.vLimitCourse != '' ? item.vLimitCourse : '無' }}<br>
                  </v-col>
                  <v-col cols="4">
                    <b>關注： </b>
                    <v-btn outlined icon v-if="isLogin && !inWachingList(item.serialNo)" @click="$emit('addWatch', item.serialNo)">
                      <v-icon>mdi-star-outline</v-icon></v-btn>
                    <v-btn outlined icon v-if="isLogin && inWachingList(item.serialNo)" @click="$emit('cancelWatch', item.serialNo)">
                      <v-icon color="yellow darken-1">mdi-star</v-icon></v-btn>
                    <b><br><br>搶課： </b>
                    <v-btn outlined icon v-if="isLogin && !inTakingList(item.serialNo)" @click="addTakeConfirm(item)">
                      <v-icon>mdi-account-plus</v-icon></v-btn>
                    <v-btn outlined icon disabled v-if="isLogin && inTakingList(item.serialNo)">
                      <v-icon>mdi-account-check-outline</v-icon></v-btn>
                  </v-col>
                </v-row>
              </v-card>
            </td>
          </template>
          <template v-else v-slot:expanded-item="{ headers, item }">
            <td :colspan="headers.length" class="pa-0">
              <v-card tile flat color="rgb(0, 0, 0, 0)" class="pl-5 pr-5 pt-0 pb-0">
                <v-row align="center">
                  <v-col cols="12">
                    <b>老師：</b> {{ item.teacher }}<br>
                    <b>備註：</b> {{ item.vComment != '' ? item.vComment : '無' }}<br>
                    <b>限制：</b> {{ item.vLimitCourse != '' ? item.vLimitCourse : '無' }}<br>
                  </v-col>
                </v-row>
              </v-card>
            </td>
          </template>
        </v-data-table>
      </v-card>
      
    </v-card>
  </v-container>
</template>

<script>  
export default {

  data () {
    return {

      noDataText: '沒有可顯示資料。',
      searching: false,
      serialNoInput: null,
      nameInput: null,
      departmentSelector: null,
      domainSelector: null,
      courses: [],
      takeConfirm: false,
      DomainNullAlert: false,
      targetCourse: null,
      targetDomain: null,

      weeks: [ '　', '一', '二', '三', '四', '五', '六', '日' ],
      periods: [ '　', '　', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'B', 'C', 'D' ],
      headers: [
        { text: '代碼', sortable: false, value: 'serialNo' },
        { text: '課程名稱', value: 'name' },
        { text: '課程時間', value: 'timeInfo' },
        { text: '', value: 'data-table-expand' }
      ],

      rules: [value => (value || '').length <= 4 || 'Max 4 characters'],

      departments: [
        /* { text: '所有系所', value: 'ALL' }, */ { text: '通識', value: 'GU' }, { text: '共同科', value: 'CU' },
        { text: '師培學院', value: 'EU' }, { text: '普通體育', value: 'PE' }, /* { text: '全人中心', value: 'VS' }, */
        { text: '教育學院', value: 'E' }, { text: '教育系', value: 'EU00' }, { text: '教育碩', value: 'EM00' },
        { text: '教育博', value: 'ED00' }, { text: '心輔系', value: 'EU01' }, { text: '心輔碩', value: 'EM01' },
        { text: '心輔博', value: 'ED01' }, { text: '社教系', value: 'EU02' }, { text: '社教碩', value: 'EM02' },
        { text: '社教博', value: 'ED02' }, { text: '衛教系', value: 'EU05' }, { text: '衛教碩', value: 'EM05' },
        { text: '衛教博', value: 'ED05' }, { text: '人發系', value: 'EU06' }, { text: '人發碩', value: 'EM06' },
        { text: '人發博', value: 'ED06' }, { text: '公領系', value: 'EU07' }, { text: '公領碩', value: 'EM07' },
        { text: '公領博', value: 'ED07' }, { text: '資訊碩', value: 'EM08' }, { text: '資訊博', value: 'ED08' },
        { text: '特教系', value: 'EU09' }, { text: '特教碩', value: 'EM09' }, { text: '特教博', value: 'ED09' },
        { text: '學習科學學位學程', value: 'EU11' }, { text: '圖資碩', value: 'EM15' }, { text: '圖資博', value: 'ED15' },
        { text: '教政碩', value: 'EM16' }, { text: '復諮碩', value: 'EM17' }, { text: '教院不分系', value: 'EU13' },
        { text: '課教碩', value: 'EM03' }, { text: '課教博', value: 'ED03' }, { text: '文學院', value: 'L' },
        { text: '國文系', value: 'LU20' }, { text: '國文碩', value: 'LM20' }, { text: '英語系', value: 'LU21' },
        { text: '英語碩', value: 'LM21' }, { text: '英語博', value: 'LD21' }, { text: '英語輔', value: 'SA21' },
        { text: '歷史系', value: 'LU22' }, { text: '歷史碩', value: 'LM22' }, { text: '歷史輔', value: 'SA22' },
        { text: '地理系', value: 'LU23' }, { text: '地理碩', value: 'LM23' }, { text: '地理博', value: 'LD23' },
        { text: '翻譯碩', value: 'LM25' }, { text: '翻譯博', value: 'LD25' }, { text: '臺文系', value: 'LU26' },
        { text: '臺文碩', value: 'LM26' }, { text: '臺史碩', value: 'LM27' }, { text: '數學系', value: 'SU40' },
        { text: '數學碩', value: 'SM40' }, { text: '物理系', value: 'SU41' }, { text: '物理碩', value: 'SM41' },
        { text: '化學系', value: 'SU42' }, { text: '化學碩', value: 'SM42' }, { text: '化學博', value: 'SD42' },
        { text: '生科系', value: 'SU43' }, { text: '生科碩', value: 'SM43' }, { text: '生科博', value: 'SD43' },
        { text: '地科系', value: 'SU44' }, { text: '地科碩', value: 'SM44' }, { text: '地科博', value: 'SD44' },
        { text: '科教碩', value: 'SM45' }, { text: '科教博', value: 'SD45' }, { text: '環教碩', value: 'SM46' },
        { text: '環教博', value: 'SD46' }, { text: '資工系', value: 'SU47' }, { text: '資工碩', value: 'SM47' },
        { text: '生物多樣學位學程', value: 'SD50' }, { text: '營養科學學位學程', value: 'SU51' },
        { text: '營養碩', value: 'SM51' }, { text: '生醫碩', value: 'SM52' }, { text: '藝術學院', value: 'T' },
        { text: '美術系', value: 'TU60' }, { text: '美術碩', value: 'TM60' }, { text: '美術博', value: 'TD60' },
        { text: '藝史碩', value: 'TM67' }, { text: '設計系', value: 'TU68' }, { text: '設計碩', value: 'TM68' },
        { text: '設計博', value: 'TD68' }, { text: '科技學院', value: 'H' }, { text: '工教系', value: 'HU70' },
        { text: '工教碩', value: 'HM70' }, { text: '工教博', value: 'HD70' }, { text: '科技系', value: 'HU71' },
        { text: '科技碩', value: 'HM71' }, { text: '科技博', value: 'HD71' }, { text: '圖傳系', value: 'HU72' },
        { text: '圖傳碩', value: 'HM72' }, { text: '機電系', value: 'HU73' }, { text: '機電碩', value: 'HM73' },
        { text: '機電博', value: 'HD73' }, { text: '電機系', value: 'HU75' }, { text: '電機碩', value: 'HM75' },
        { text: '車能學位學程', value: 'HU76' }, { text: '光電工程學位學程', value: 'HU77' },
        { text: '光電碩', value: 'HM77' }, { text: '運休學院', value: 'A' }, { text: '體育系', value: 'AU30' },
        { text: '體育碩', value: 'AM30' }, { text: '體育博', value: 'AD30' }, { text: '休旅碩', value: 'AM31' },
        { text: '休旅博', value: 'AD31' }, { text: '競技系', value: 'AU32' }, { text: '競技碩', value: 'AM32' },
        { text: '國社學院', value: 'I' }, { text: '歐文碩', value: 'IM82' }, { text: '東亞系', value: 'IU83' },
        { text: '東亞碩', value: 'IM83' }, { text: '東亞博', value: 'ID83' }, { text: '華語系', value: 'IU84' },
        { text: '華語碩', value: 'IM84' }, { text: '華語博', value: 'ID84' }, { text: '人資碩', value: 'IM86' },
        { text: '政治碩', value: 'IM87' }, { text: '大傳碩', value: 'IM88' }, { text: '社工碩', value: 'IM89' },
        { text: '音樂系', value: 'MU90' }, { text: '音樂碩', value: 'MM90' }, { text: '音樂博', value: 'MD90' },
        { text: '民音碩', value: 'MM91' }, { text: '表演學位學程', value: 'MU92' }, { text: '表演碩', value: 'MM92' },
        { text: '管理學院', value: 'O' }, { text: '管理碩', value: 'OM55' }, { text: '全營碩', value: 'OM56' },
        { text: '企管系', value: 'OU57' }, { text: '戶外探索領導學程', value: 'ZU66' },
        { text: '科學計算學程', value: 'ZU67' }, { text: '太陽能源與工程學程', value: 'ZU68' },
        { text: '文物保存修復學分學程', value: 'ZU69' }, { text: '運動傷害防護學程', value: 'ZU73' },
        { text: '國際教師學程-華語文', value: 'ZU74' }, { text: '國際教師學程-數學', value: 'ZU75' },
        { text: '國際教師學程-物理', value: 'ZU76' }, { text: '資訊科技應用學程', value: 'ZU77' },
        { text: '人工智慧技術與應用學', value: 'ZU78' }, { text: 'PASSION偏鄉教育學程', value: 'ZU79' },
        { text: '基礎管理學程', value: 'ZU83' }, { text: '財金學程', value: 'ZU84' },
        { text: '影音藝術學程', value: 'ZU88' }, { text: '環境監測學程', value: 'ZU89' },
        { text: '榮譽英語學程', value: 'ZU92' }, { text: '歐洲文化學程', value: 'ZU93' },
        { text: '文學創作學程', value: 'ZU94' }, { text: '日語學程', value: 'ZU97' }, { text: '高齡學程', value: 'ZU98' },
        { text: '區域學程', value: 'ZU9A' }, { text: '空間學程', value: 'ZU9B' },
        { text: '學校心理學學程', value: 'ZU9C' }, { text: '社會與傳播學程', value: 'ZU9E' },
        { text: '大數據學程', value: 'ZU9K' }, { text: '室內設計學程', value: 'ZU9O' },
        { text: '韓語學程', value: 'ZU9P' }, { text: '社團領導學程', value: 'ZU9Q' },
        { text: '國際文化學程', value: 'ZU9R' }, { text: '兒童雙語學程', value: 'ZU9T' },
        { text: '原民教育學程', value: 'ZU9U' }, { text: '大師創業學程', value: 'ZU9V' },
        { text: '金牌書院', value: 'ZU9W' }, { text: '哲學學程', value: 'ZU9X' }, { text: '藝術產業學程', value: 'ZU9Y' },
        { text: '國際教師學程-國際', value: 'ZU9Z' }, { text: '校際學士班(臺大)', value: '9UAA'},
        { text: '校際學士班（臺科大）', value: '9UAB' }
      ],
      domains: [
        /* { text: 'ALL', value: 'ALL' }, */
        { text: '語言與文學', value: '00UG' },
        { text: '藝術與美感', value: '01UG' },
        { text: '哲學思維與道德推理', value: '02UG' },
        { text: '公民素養與社會探究', value: '03UG' },
        { text: '歷史與文化', value: '04UG' },
        { text: '數學與邏輯思維', value: '05UG' },
        { text: '科學與生命', value: '06UG' },
        { text: '第二外語', value: '07UG' },
        { text: '生活技能', value: '08UG' },
        { text: '自主學習', value: '09UG' }
      ],
      times: [
        [ false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false ],
        [ false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false ],
        [ false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false ],
        [ false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false ],
        [ false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false ],
        [ false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false ],
        [ false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false ],
        [ false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false ]
      ]

    }
  },

  props: ['isLogin', 'searchAlert', 'takeResult', 'watchingList', 'takingList'],
  
  methods: {

    searchCourses () {
      this.searching = true
      this.$http.post(`/api/search`,
        {
          'serialNo': this.serialNoInput != '' ? this.serialNoInput : null ,
          'deptCode': this.departmentSelector,
          'domnCode': this.domnCode,
          'name': this.nameInput != '' ? this.nameInput : null,
          'time':this.times
        }
      )
        .then((res) => {
          this.courses = res.data.data
          this.searching = false
        })
        .catch((err) => {
          console.log('err: ', err)
          this.courses = []
          this.searching = false
        })
    },

    inWachingList (serialNo) {
      var i
      for (i = 0; i < this.watchingList.length; i++) {
        if (serialNo == this.watchingList[i]) return true
      }
      return false
    },

    inTakingList (serialNo) {
      var i
      for (i = 0; i < this.takingList.length; i++) {
        if (serialNo == this.takingList[i]) return true
      }
      return false
    },

    addTakeConfirm (course) {
      this.targetCourse = course
      this.takeConfirm = true
    },

    addTake () {
      // wait for develop
      // if (this.targetCourse.deptCode == 'GU' && domainwrong) {}
      // else {}

      if (this.targetCourse.deptCode == 'GU' && this.targetDomain == null) {
        this.DomainNullAlert = true
        return
      }

      this.takeConfirm = false
      this.$emit('addTake', this.targetCourse, this.targetDomain)
      this.targetCourse = null
      this.targetDomain = null
    }

  }
  
}
</script>

<style></style>
