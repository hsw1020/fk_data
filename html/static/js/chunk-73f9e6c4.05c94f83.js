(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-73f9e6c4"],{9139:function(t,e,i){"use strict";i.d(e,"h",(function(){return o})),i.d(e,"i",(function(){return a})),i.d(e,"g",(function(){return s})),i.d(e,"f",(function(){return r})),i.d(e,"a",(function(){return n})),i.d(e,"e",(function(){return c})),i.d(e,"d",(function(){return d})),i.d(e,"b",(function(){return u})),i.d(e,"c",(function(){return f}));var l=i("b775");function o(t){return Object(l["a"])({url:"indicator/query/json/",method:"get",params:t})}function a(t){return Object(l["a"])({url:"indicator/query/json/",method:"get",params:t})}function s(t){return Object(l["a"])({url:"indicator/query/list/",method:"get"})}function r(t){return Object(l["a"])({url:"/indicator/add/",method:"get",params:t})}function n(t){return Object(l["a"])({url:"indicator/del",method:"get",params:t})}function c(t){return Object(l["a"])({url:"indicator/edit/",method:"post",data:t})}function d(t){return Object(l["a"])({url:"indicator/edit/",method:"get",params:t})}function u(t){return Object(l["a"])({url:"model/download/",method:"get",responseType:"blob",params:t})}function f(t){return Object(l["a"])({url:"indicator/edit/",method:"get",params:t})}},d849:function(t,e,i){"use strict";i.r(e);var l=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"app-container"},[i("div",{staticClass:"filter-container"},[i("span",{staticStyle:{float:"right"}},[i("router-link",{staticClass:"link-type",attrs:{to:"/indicator/create/"}}),i("el-button",{staticClass:"filter-item",staticStyle:{"margin-left":"10px"},attrs:{type:"primary",size:"mini",icon:"el-icon-plus",plain:""},on:{click:t.handleCreate}},[t._v(" 新建指标 ")])],1)]),i("el-table",{staticStyle:{width:"100%"},attrs:{data:t.indicatorList.slice(t.pageSize*(t.currentPage-1),t.pageSize*t.currentPage)}},[i("el-table-column",{attrs:{label:"序号",width:"90"},scopedSlots:t._u([{key:"default",fn:function(e){return[i("span",[t._v(t._s(e.$index+1+t.pageSize*(t.currentPage-1)))])]}}])}),i("el-table-column",{attrs:{prop:"field",label:"评价主题"}}),i("el-table-column",{attrs:{prop:"scope",label:"评价对象"}}),i("el-table-column",{attrs:{prop:"create_by",label:"创建者"}}),i("el-table-column",{attrs:{prop:"create_time",label:"创建时间"}}),i("el-table-column",{attrs:{prop:"update_by",label:"更新者"}}),i("el-table-column",{attrs:{prop:"updateTime",label:"更新时间"}}),i("el-table-column",{attrs:{label:"操作"},scopedSlots:t._u([{key:"default",fn:function(e){var l=e.row;return[i("el-button",{attrs:{type:"text",size:"small"},on:{click:function(e){return e.preventDefault(),t.detailClick(l)}}},[t._v("查看")]),i("el-button",{attrs:{type:"text",size:"small"},on:{click:function(e){return e.preventDefault(),t.editClick(l)}}},[t._v("编辑")]),i("el-button",{attrs:{type:"text",size:"small"},on:{click:function(e){return e.preventDefault(),t.deleteClick(l)}}},[t._v("删除")])]}}])})],1),i("el-row",{staticClass:"table-pagination",attrs:{gutter:20}},[i("el-col",{staticClass:"pagination-text",attrs:{span:12,offset:6}},[i("div"),i("el-pagination",{attrs:{background:"","current-page":t.currentPage,layout:"total, prev, pager, next",total:t.total,"page-size":t.pageSize},on:{"current-change":t.handleCurrentChange}})],1)],1),i("el-dialog",{attrs:{title:"新建指标",visible:t.dialogTableVisible_add},on:{"update:visible":function(e){t.dialogTableVisible_add=e},close:t.handleClose}},[i("el-form",{ref:"addForm",attrs:{model:t.form,"label-width":"80px","validate-on-rule-change":!1,size:"mini"}},[i("el-form-item",{attrs:{label:"评价主题",prop:"fieldList"}},[i("el-select",{attrs:{multiple:!1,filterable:"","allow-create":"","default-first-option":"",placeholder:"请选择或输入评价主题"},on:{change:t.changeField},model:{value:t.form.fieldList,callback:function(e){t.$set(t.form,"fieldList",e)},expression:"form.fieldList"}},t._l(t.form.fieldOptions,(function(t){return i("el-option",{key:t.value,attrs:{label:t.label,value:t.value,disabled:t.disabled}})})),1)],1),i("el-form-item",{attrs:{label:"评价对象",prop:"scopeList"}},[i("el-select",{attrs:{multiple:!1,filterable:"","allow-create":"","default-first-option":"",placeholder:"请选择或输入评价对象"},on:{change:t.changeScope},model:{value:t.form.scopeList,callback:function(e){t.$set(t.form,"scopeList",e)},expression:"form.scopeList"}},t._l(t.form.scopeOptions,(function(t){return i("el-option",{key:t.value,attrs:{label:t.label,value:t.value,disabled:t.disabled}})})),1)],1),i("el-form-item",{attrs:{label:"评价体系",prop:"resource"}},[i("el-radio-group",{model:{value:t.form.resource,callback:function(e){t.$set(t.form,"resource",e)},expression:"form.resource"}},[i("el-radio",{attrs:{label:"导入默认指标体系模板"}}),i("el-radio",{attrs:{label:"导入指标体系Excel文件"}})],1)],1),"导入指标体系Excel文件"===t.form.resource?i("el-form-item",{attrs:{label:""}},[i("el-row",{attrs:{gutter:20}},[i("el-col",{attrs:{span:16}},[i("div",{staticClass:"grid-content bg-purple"},[i("el-upload",{ref:"upload",staticClass:"upload-demo",attrs:{action:t.baseURL,drag:"",multiple:!1,data:t.upData,accept:".xlsx,.xls","auto-upload":!1,"file-list":t.fileList,limit:1,"before-upload":t.beforeXlsxUpload}},[i("i",{staticClass:"el-icon-upload"}),i("div",{staticClass:"el-upload__text"},[t._v("将文件拖到此处，或"),i("em",[t._v("点击上传")])]),i("div",{staticClass:"el-upload__tip",attrs:{slot:"tip"},slot:"tip"},[t._v("只能上传后缀名为.xlsx , .xls文件")])])],1)]),i("el-col",{attrs:{span:5}},[i("div",{staticClass:"grid-content bg-purple"},[i("el-button",{attrs:{type:"text",icon:"el-icon-download",disabled:!t.form.fieldList},on:{click:t.downloadTemplate}},[t._v("下载模板")])],1)])],1)],1):t._e(),i("el-form-item",[i("el-button",{attrs:{type:"primary",disabled:!(t.form.resource&&t.form.scopeList&&t.form.fieldList)},on:{click:t.onSubmit}},[t._v("确定")]),i("el-button",{on:{click:function(e){t.dialogTableVisible_add=!1}}},[t._v("取消")])],1)],1)],1),i("el-dialog",{attrs:{title:"删除指标",visible:t.dialogTableVisible_del},on:{"update:visible":function(e){t.dialogTableVisible_del=e}}},[i("h3",[i("i",{staticClass:"el-icon-warning",staticStyle:{color:"red"}}),t._v(" 确认删除以下指标吗？删除指标后，指标的数据将一起被删除！")]),i("el-row",{staticClass:"table-pagination",attrs:{gutter:20}},[i("el-col",{attrs:{span:24}},[i("div",{staticStyle:{border:"1px solid #E4E7ED","padding-left":"10px"}},[i("el-main",[i("el-form",{staticClass:"demo-form-inline",attrs:{size:"mini"}},[i("el-form-item",{attrs:{label:"评价主题:"}},[t._v(" "+t._s(t.currentIndicator.field)+" ")]),i("el-form-item",{attrs:{label:"评价对象:"}},[t._v(" "+t._s(t.currentIndicator.scope)+" ")])],1)],1),i("el-footer",[i("el-row",{attrs:{type:"flex",justify:"start"}},[i("el-link",{attrs:{type:"info",underline:!1}},[t._v("创建者："+t._s(t.currentIndicator.create_by)+"，创建时间："+t._s(t.currentIndicator.create_time))])],1),i("el-row",{attrs:{type:"flex",justify:"start"}},[i("el-link",{attrs:{type:"info",underline:!1}},[t._v("更新者："+t._s(t.currentIndicator.update_by)+"，更新时间："+t._s(t.currentIndicator.updateTime))])],1)],1)],1)])],1),i("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{attrs:{size:"mini"},on:{click:function(e){t.dialogTableVisible_del=!1}}},[t._v("取 消")]),i("el-button",{attrs:{type:"primary",size:"mini"},on:{click:function(e){return t.deleteIndicator()}}},[t._v("确 定")])],1)],1)],1)},o=[],a=i("5530"),s=(i("a630"),i("3ca3"),i("d3b7"),i("6062"),i("ddb0"),i("d81d"),i("4de4"),i("159b"),i("2b3d"),i("2f62")),r=i("9139"),n=i("ed08"),c={data:function(){return{dialogTableVisible_add:!1,dialogTableVisible_del:!1,FileisLt500KB:!1,fileList:[],upData:{},currentPage:1,pageSize:10,total:0,indicatorList:[],defaultScopeOptions:[],defaultFieldOptions:[],fieldOptions:[],scopeOptions:[],baseURL:"",form:{scopeList:[],fieldList:[],resource:"",fieldOptions:[],scopeOptions:[]},tableData:[]}},computed:Object(a["a"])({},Object(s["b"])(["scope","field","currentIndicator"])),mounted:function(){this.fetchData(),this.baseURL="http://127.0.0.1:9095/mxk/indicator/add/"},methods:{fetchData:function(){var t=this;Object(r["g"])().then((function(e){t.indicatorList=e.data,t.total=e.data.length;var i=t.getArrayProps(t.indicatorList,"field");i=Array.from(new Set(i)),console.log(i);var l=t.getArrayProps(t.indicatorList,"scope");l=Array.from(new Set(l)),t.form.fieldOptions=[],console.log(l),i.map((function(e,i){var o={},a={};o.value=e,o.label=e,a.value=e,a.label=e,o.id=i,o.scopeList=[],l.map((function(i){var l={};l.value=i,l.label=i,t.indicatorList.map((function(t){t.field===e&&t.scope===i&&(l.disabled=!0)})),o.scopeList.push(l)})),t.defaultFieldOptions.push(a),t.fieldOptions.push(o)})),l.map((function(e,l){var o={},a={};o.value=e,o.label=e,a.value=e,a.label=e,o.id=e,o.fieldList=[],i.map((function(i){var a={};a.value=i,a.label=i,a.id=l,t.indicatorList.map((function(t){t.field===i&&t.scope===e&&(a.disabled=!0)})),o.fieldList.push(a)})),t.defaultScopeOptions.push(a),t.scopeOptions.push(o)})),t.form.fieldOptions=t.defaultFieldOptions,t.form.scopeOptions=t.defaultScopeOptions,console.log(t.form)}))},changeField:function(){var t=this;console.log(this.form.fieldList),console.log(this.fieldOptions);var e=this.fieldOptions.filter((function(e){return e.value===t.form.fieldList}));this.form.scopeOptions=e.length?e[0].scopeList:this.defaultScopeOptions},changeScope:function(){var t=this;console.log(this.form.scopeList),console.log(this.scopeOptions);var e=this.scopeOptions.filter((function(e){return e.value===t.form.scopeList}));console.log(e),this.form.fieldOptions=e.length?e[0].fieldList:this.defaultFieldOptions},getArrayProps:function(t,e){e=e||"value";var i=[];return t&&t.forEach((function(t){i.push(t[e])})),i},downloadTemplate:function(){var t=this;console.log(this.form.fieldList);var e=this.form.fieldList,i={field:e};Object(r["b"])(i).then((function(t){var i=window.URL.createObjectURL(new Blob([t])),l=document.createElement("a");l.style.display="none",l.href=i,l.setAttribute("download",e+"指标模板.xls"),document.body.appendChild(l),l.click()})).catch((function(){t.$message.error("网络错误!")}))},setTagsViewTitle:function(t){var e="编辑指标",i=Object.assign({},this.tempRoute,{title:"".concat(e,"-").concat(t)});console.log(i),this.$store.dispatch("tagsView/updateVisitedView",i)},editClick:function(t){this.$store.dispatch("system/changeCurrentIndicator",t),this.$router.push("/indicator/edit/"+t.indicator_id)},detailClick:function(t){this.$store.dispatch("system/changeCurrentIndicator",t),this.$router.push("/indicator/detail")},deleteClick:function(t){this.dialogTableVisible_del=!0,this.$store.dispatch("system/changeCurrentIndicator",t)},deleteIndicator:function(){var t=this,e={field:this.currentIndicator.field,scope:this.currentIndicator.scope};Object(r["a"])(e).then((function(t){console.log(t)})),setTimeout((function(){t.fetchData()}),200),this.dialogTableVisible_del=!1},handleClick:function(t){console.log(t)},handleCreate:function(){this.dialogTableVisible_add=!0},handleClose:function(){this.FileisLt500KB=!1,console.log(this.$refs["addForm"]),this.$refs["addForm"].resetFields()},beforeXlsxUpload:function(t){console.log(t);var e=t.size/1024+"KB";return this.FileisLt500KB=t.size/1024<500,console.log("this.FileisLt500KB",this.FileisLt500KB),this.FileisLt500KB||this.$message.error("上传文件大小不能超过 500KB!,您所上传文件大小为"+e),this.FileisLt500KB},onSubmit:function(){var t=this;if(this.$set(this.upData,"scope",this.form.scopeList),this.$set(this.upData,"field",this.form.fieldList),console.log("导入指标体系Excel文件"===this.form.resource),console.log("导入默认指标体系模板"===this.form.resource),"导入指标体系Excel文件"===this.form.resource)this.$refs.upload.submit();else if("导入默认指标体系模板"===this.form.resource){var e={field:this.form.fieldList,scope:this.form.scopeList};Object(r["f"])(e).then((function(t){console.log(t)})).catch((function(){t.$message.error("网络错误!")}))}var i=new Date;this.$store.dispatch("system/changeCurrentIndicator",{field:this.form.fieldList,scope:this.form.scopeList,create_by:"",create_time:Object(n["b"])(i,"{y}-{m}-{d} {h}:{i}"),update_by:"",updateTime:Object(n["b"])(i,"{y}-{m}-{d} {h}:{i}")}),this.handleClose(),this.$router.push("/indicator/create/")},handleCurrentChange:function(t){console.log("当前页: ".concat(t)),this.currentPage=t}}},d=c,u=i("2877"),f=Object(u["a"])(d,l,o,!1,null,null,null);e["default"]=f.exports}}]);