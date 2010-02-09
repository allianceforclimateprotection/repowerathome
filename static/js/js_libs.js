/*
 * jQuery JavaScript Library v1.4.1
 * http://jquery.com/
 *
 * Copyright 2010, John Resig
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://jquery.org/license
 *
 * Includes Sizzle.js
 * http://sizzlejs.com/
 * Copyright 2010, The Dojo Foundation
 * Released under the MIT, BSD, and GPL Licenses.
 *
 * Date: Mon Jan 25 19:43:33 2010 -0500
 */
(function(aI,B){var a=function(aU,aV){return new a.fn.init(aU,aV)},n=aI.jQuery,Q=aI.$,aa=aI.document,W,O=/^[^<]*(<[\w\W]+>)[^>]*$|^#([\w-]+)$/,aS=/^.[^:#\[\.,]*$/,au=/\S/,L=/^(\s|\u00A0)+|(\s|\u00A0)+$/g,e=/^<(\w+)\s*\/?>(?:<\/\1>)?$/,b=navigator.userAgent,u,I=false,ac=[],aC,aq=Object.prototype.toString,an=Object.prototype.hasOwnProperty,g=Array.prototype.push,D=Array.prototype.slice,s=Array.prototype.indexOf;a.fn=a.prototype={init:function(aU,aX){var aW,aY,aV,aZ;if(!aU){return this}if(aU.nodeType){this.context=this[0]=aU;this.length=1;return this}if(typeof aU==="string"){aW=O.exec(aU);if(aW&&(aW[1]||!aX)){if(aW[1]){aZ=(aX?aX.ownerDocument||aX:aa);aV=e.exec(aU);if(aV){if(a.isPlainObject(aX)){aU=[aa.createElement(aV[1])];a.fn.attr.call(aU,aX,true)}else{aU=[aZ.createElement(aV[1])]}}else{aV=H([aW[1]],[aZ]);aU=(aV.cacheable?aV.fragment.cloneNode(true):aV.fragment).childNodes}}else{aY=aa.getElementById(aW[2]);if(aY){if(aY.id!==aW[2]){return W.find(aU)}this.length=1;this[0]=aY}this.context=aa;this.selector=aU;return this}}else{if(!aX&&/^\w+$/.test(aU)){this.selector=aU;this.context=aa;aU=aa.getElementsByTagName(aU)}else{if(!aX||aX.jquery){return(aX||W).find(aU)}else{return a(aX).find(aU)}}}}else{if(a.isFunction(aU)){return W.ready(aU)}}if(aU.selector!==B){this.selector=aU.selector;this.context=aU.context}return a.isArray(aU)?this.setArray(aU):a.makeArray(aU,this)},selector:"",jquery:"1.4.1",length:0,size:function(){return this.length},toArray:function(){return D.call(this,0)},get:function(aU){return aU==null?this.toArray():(aU<0?this.slice(aU)[0]:this[aU])},pushStack:function(aV,aX,aU){var aW=a(aV||null);aW.prevObject=this;aW.context=this.context;if(aX==="find"){aW.selector=this.selector+(this.selector?" ":"")+aU}else{if(aX){aW.selector=this.selector+"."+aX+"("+aU+")"}}return aW},setArray:function(aU){this.length=0;g.apply(this,aU);return this},each:function(aV,aU){return a.each(this,aV,aU)},ready:function(aU){a.bindReady();if(a.isReady){aU.call(aa,a)}else{if(ac){ac.push(aU)}}return this},eq:function(aU){return aU===-1?this.slice(aU):this.slice(aU,+aU+1)},first:function(){return this.eq(0)},last:function(){return this.eq(-1)},slice:function(){return this.pushStack(D.apply(this,arguments),"slice",D.call(arguments).join(","))},map:function(aU){return this.pushStack(a.map(this,function(aW,aV){return aU.call(aW,aV,aW)}))},end:function(){return this.prevObject||a(null)},push:g,sort:[].sort,splice:[].splice};a.fn.init.prototype=a.fn;a.extend=a.fn.extend=function(){var aZ=arguments[0]||{},aY=1,aX=arguments.length,a1=false,a2,aW,aU,aV;if(typeof aZ==="boolean"){a1=aZ;aZ=arguments[1]||{};aY=2}if(typeof aZ!=="object"&&!a.isFunction(aZ)){aZ={}}if(aX===aY){aZ=this;--aY}for(;aY<aX;aY++){if((a2=arguments[aY])!=null){for(aW in a2){aU=aZ[aW];aV=a2[aW];if(aZ===aV){continue}if(a1&&aV&&(a.isPlainObject(aV)||a.isArray(aV))){var a0=aU&&(a.isPlainObject(aU)||a.isArray(aU))?aU:a.isArray(aV)?[]:{};aZ[aW]=a.extend(a1,a0,aV)}else{if(aV!==B){aZ[aW]=aV}}}}}return aZ};a.extend({noConflict:function(aU){aI.$=Q;if(aU){aI.jQuery=n}return a},isReady:false,ready:function(){if(!a.isReady){if(!aa.body){return setTimeout(a.ready,13)}a.isReady=true;if(ac){var aV,aU=0;while((aV=ac[aU++])){aV.call(aa,a)}ac=null}if(a.fn.triggerHandler){a(aa).triggerHandler("ready")}}},bindReady:function(){if(I){return}I=true;if(aa.readyState==="complete"){return a.ready()}if(aa.addEventListener){aa.addEventListener("DOMContentLoaded",aC,false);aI.addEventListener("load",a.ready,false)}else{if(aa.attachEvent){aa.attachEvent("onreadystatechange",aC);aI.attachEvent("onload",a.ready);var aU=false;try{aU=aI.frameElement==null}catch(aV){}if(aa.documentElement.doScroll&&aU){w()}}}},isFunction:function(aU){return aq.call(aU)==="[object Function]"},isArray:function(aU){return aq.call(aU)==="[object Array]"},isPlainObject:function(aV){if(!aV||aq.call(aV)!=="[object Object]"||aV.nodeType||aV.setInterval){return false}if(aV.constructor&&!an.call(aV,"constructor")&&!an.call(aV.constructor.prototype,"isPrototypeOf")){return false}var aU;for(aU in aV){}return aU===B||an.call(aV,aU)},isEmptyObject:function(aV){for(var aU in aV){return false}return true},error:function(aU){throw aU},parseJSON:function(aU){if(typeof aU!=="string"||!aU){return null}if(/^[\],:{}\s]*$/.test(aU.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,"@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,"]").replace(/(?:^|:|,)(?:\s*\[)+/g,""))){return aI.JSON&&aI.JSON.parse?aI.JSON.parse(aU):(new Function("return "+aU))()}else{a.error("Invalid JSON: "+aU)}},noop:function(){},globalEval:function(aW){if(aW&&au.test(aW)){var aV=aa.getElementsByTagName("head")[0]||aa.documentElement,aU=aa.createElement("script");aU.type="text/javascript";if(a.support.scriptEval){aU.appendChild(aa.createTextNode(aW))}else{aU.text=aW}aV.insertBefore(aU,aV.firstChild);aV.removeChild(aU)}},nodeName:function(aV,aU){return aV.nodeName&&aV.nodeName.toUpperCase()===aU.toUpperCase()},each:function(aX,a1,aW){var aV,aY=0,aZ=aX.length,aU=aZ===B||a.isFunction(aX);if(aW){if(aU){for(aV in aX){if(a1.apply(aX[aV],aW)===false){break}}}else{for(;aY<aZ;){if(a1.apply(aX[aY++],aW)===false){break}}}}else{if(aU){for(aV in aX){if(a1.call(aX[aV],aV,aX[aV])===false){break}}}else{for(var a0=aX[0];aY<aZ&&a1.call(a0,aY,a0)!==false;a0=aX[++aY]){}}}return aX},trim:function(aU){return(aU||"").replace(L,"")},makeArray:function(aW,aV){var aU=aV||[];if(aW!=null){if(aW.length==null||typeof aW==="string"||a.isFunction(aW)||(typeof aW!=="function"&&aW.setInterval)){g.call(aU,aW)}else{a.merge(aU,aW)}}return aU},inArray:function(aW,aX){if(aX.indexOf){return aX.indexOf(aW)}for(var aU=0,aV=aX.length;aU<aV;aU++){if(aX[aU]===aW){return aU}}return -1},merge:function(aY,aW){var aX=aY.length,aV=0;if(typeof aW.length==="number"){for(var aU=aW.length;aV<aU;aV++){aY[aX++]=aW[aV]}}else{while(aW[aV]!==B){aY[aX++]=aW[aV++]}}aY.length=aX;return aY},grep:function(aV,aZ,aU){var aW=[];for(var aX=0,aY=aV.length;aX<aY;aX++){if(!aU!==!aZ(aV[aX],aX)){aW.push(aV[aX])}}return aW},map:function(aV,a0,aU){var aW=[],aZ;for(var aX=0,aY=aV.length;aX<aY;aX++){aZ=a0(aV[aX],aX,aU);if(aZ!=null){aW[aW.length]=aZ}}return aW.concat.apply([],aW)},guid:1,proxy:function(aW,aV,aU){if(arguments.length===2){if(typeof aV==="string"){aU=aW;aW=aU[aV];aV=B}else{if(aV&&!a.isFunction(aV)){aU=aV;aV=B}}}if(!aV&&aW){aV=function(){return aW.apply(aU||this,arguments)}}if(aW){aV.guid=aW.guid=aW.guid||aV.guid||a.guid++}return aV},uaMatch:function(aV){aV=aV.toLowerCase();var aU=/(webkit)[ \/]([\w.]+)/.exec(aV)||/(opera)(?:.*version)?[ \/]([\w.]+)/.exec(aV)||/(msie) ([\w.]+)/.exec(aV)||!/compatible/.test(aV)&&/(mozilla)(?:.*? rv:([\w.]+))?/.exec(aV)||[];return{browser:aU[1]||"",version:aU[2]||"0"}},browser:{}});u=a.uaMatch(b);if(u.browser){a.browser[u.browser]=true;a.browser.version=u.version}if(a.browser.webkit){a.browser.safari=true}if(s){a.inArray=function(aU,aV){return s.call(aV,aU)}}W=a(aa);if(aa.addEventListener){aC=function(){aa.removeEventListener("DOMContentLoaded",aC,false);a.ready()}}else{if(aa.attachEvent){aC=function(){if(aa.readyState==="complete"){aa.detachEvent("onreadystatechange",aC);a.ready()}}}}function w(){if(a.isReady){return}try{aa.documentElement.doScroll("left")}catch(aU){setTimeout(w,1);return}a.ready()}function aR(aU,aV){if(aV.src){a.ajax({url:aV.src,async:false,dataType:"script"})}else{a.globalEval(aV.text||aV.textContent||aV.innerHTML||"")}if(aV.parentNode){aV.parentNode.removeChild(aV)}}function al(aU,a2,a0,aW,aZ,a1){var aV=aU.length;if(typeof a2==="object"){for(var aX in a2){al(aU,aX,a2[aX],aW,aZ,a0)}return aU}if(a0!==B){aW=!a1&&aW&&a.isFunction(a0);for(var aY=0;aY<aV;aY++){aZ(aU[aY],a2,aW?a0.call(aU[aY],aY,aZ(aU[aY],a2)):a0,a1)}return aU}return aV?aZ(aU[0],a2):null}function aL(){return(new Date).getTime()}(function(){a.support={};var a0=aa.documentElement,aZ=aa.createElement("script"),aU=aa.createElement("div"),aV="script"+aL();aU.style.display="none";aU.innerHTML="   <link/><table></table><a href='/a' style='color:red;float:left;opacity:.55;'>a</a><input type='checkbox'/>";var a2=aU.getElementsByTagName("*"),a1=aU.getElementsByTagName("a")[0];if(!a2||!a2.length||!a1){return}a.support={leadingWhitespace:aU.firstChild.nodeType===3,tbody:!aU.getElementsByTagName("tbody").length,htmlSerialize:!!aU.getElementsByTagName("link").length,style:/red/.test(a1.getAttribute("style")),hrefNormalized:a1.getAttribute("href")==="/a",opacity:/^0.55$/.test(a1.style.opacity),cssFloat:!!a1.style.cssFloat,checkOn:aU.getElementsByTagName("input")[0].value==="on",optSelected:aa.createElement("select").appendChild(aa.createElement("option")).selected,checkClone:false,scriptEval:false,noCloneEvent:true,boxModel:null};aZ.type="text/javascript";try{aZ.appendChild(aa.createTextNode("window."+aV+"=1;"))}catch(aX){}a0.insertBefore(aZ,a0.firstChild);if(aI[aV]){a.support.scriptEval=true;delete aI[aV]}a0.removeChild(aZ);if(aU.attachEvent&&aU.fireEvent){aU.attachEvent("onclick",function a3(){a.support.noCloneEvent=false;aU.detachEvent("onclick",a3)});aU.cloneNode(true).fireEvent("onclick")}aU=aa.createElement("div");aU.innerHTML="<input type='radio' name='radiotest' checked='checked'/>";var aW=aa.createDocumentFragment();aW.appendChild(aU.firstChild);a.support.checkClone=aW.cloneNode(true).cloneNode(true).lastChild.checked;a(function(){var a4=aa.createElement("div");a4.style.width=a4.style.paddingLeft="1px";aa.body.appendChild(a4);a.boxModel=a.support.boxModel=a4.offsetWidth===2;aa.body.removeChild(a4).style.display="none";a4=null});var aY=function(a4){var a6=aa.createElement("div");a4="on"+a4;var a5=(a4 in a6);if(!a5){a6.setAttribute(a4,"return;");a5=typeof a6[a4]==="function"}a6=null;return a5};a.support.submitBubbles=aY("submit");a.support.changeBubbles=aY("change");a0=aZ=aU=a2=a1=null})();a.props={"for":"htmlFor","class":"className",readonly:"readOnly",maxlength:"maxLength",cellspacing:"cellSpacing",rowspan:"rowSpan",colspan:"colSpan",tabindex:"tabIndex",usemap:"useMap",frameborder:"frameBorder"};var aE="jQuery"+aL(),aD=0,aP={};var K={};a.extend({cache:{},expando:aE,noData:{embed:true,object:true,applet:true},data:function(aW,aV,aY){if(aW.nodeName&&a.noData[aW.nodeName.toLowerCase()]){return}aW=aW==aI?aP:aW;var aZ=aW[aE],aU=a.cache,aX;if(!aV&&!aZ){return null}if(!aZ){aZ=++aD}if(typeof aV==="object"){aW[aE]=aZ;aX=aU[aZ]=a.extend(true,{},aV)}else{if(aU[aZ]){aX=aU[aZ]}else{if(typeof aY==="undefined"){aX=K}else{aX=aU[aZ]={}}}}if(aY!==B){aW[aE]=aZ;aX[aV]=aY}return typeof aV==="string"?aX[aV]:aX},removeData:function(aW,aV){if(aW.nodeName&&a.noData[aW.nodeName.toLowerCase()]){return}aW=aW==aI?aP:aW;var aZ=aW[aE],aU=a.cache,aX=aU[aZ];if(aV){if(aX){delete aX[aV];if(a.isEmptyObject(aX)){a.removeData(aW)}}}else{try{delete aW[aE]}catch(aY){if(aW.removeAttribute){aW.removeAttribute(aE)}}delete aU[aZ]}}});a.fn.extend({data:function(aU,aW){if(typeof aU==="undefined"&&this.length){return a.data(this[0])}else{if(typeof aU==="object"){return this.each(function(){a.data(this,aU)})}}var aX=aU.split(".");aX[1]=aX[1]?"."+aX[1]:"";if(aW===B){var aV=this.triggerHandler("getData"+aX[1]+"!",[aX[0]]);if(aV===B&&this.length){aV=a.data(this[0],aU)}return aV===B&&aX[1]?this.data(aX[0]):aV}else{return this.trigger("setData"+aX[1]+"!",[aX[0],aW]).each(function(){a.data(this,aU,aW)})}},removeData:function(aU){return this.each(function(){a.removeData(this,aU)})}});a.extend({queue:function(aV,aU,aX){if(!aV){return}aU=(aU||"fx")+"queue";var aW=a.data(aV,aU);if(!aX){return aW||[]}if(!aW||a.isArray(aX)){aW=a.data(aV,aU,a.makeArray(aX))}else{aW.push(aX)}return aW},dequeue:function(aX,aW){aW=aW||"fx";var aU=a.queue(aX,aW),aV=aU.shift();if(aV==="inprogress"){aV=aU.shift()}if(aV){if(aW==="fx"){aU.unshift("inprogress")}aV.call(aX,function(){a.dequeue(aX,aW)})}}});a.fn.extend({queue:function(aU,aV){if(typeof aU!=="string"){aV=aU;aU="fx"}if(aV===B){return a.queue(this[0],aU)}return this.each(function(aX,aY){var aW=a.queue(this,aU,aV);if(aU==="fx"&&aW[0]!=="inprogress"){a.dequeue(this,aU)}})},dequeue:function(aU){return this.each(function(){a.dequeue(this,aU)})},delay:function(aV,aU){aV=a.fx?a.fx.speeds[aV]||aV:aV;aU=aU||"fx";return this.queue(aU,function(){var aW=this;setTimeout(function(){a.dequeue(aW,aU)},aV)})},clearQueue:function(aU){return this.queue(aU||"fx",[])}});var am=/[\n\t]/g,R=/\s+/,at=/\r/g,aM=/href|src|style/,d=/(button|input)/i,y=/(button|input|object|select|textarea)/i,j=/^(a|area)$/i,G=/radio|checkbox/;a.fn.extend({attr:function(aU,aV){return al(this,aU,aV,true,a.attr)},removeAttr:function(aU,aV){return this.each(function(){a.attr(this,aU,"");if(this.nodeType===1){this.removeAttribute(aU)}})},addClass:function(aZ){if(a.isFunction(aZ)){return this.each(function(a3){var a2=a(this);a2.addClass(aZ.call(this,a3,a2.attr("class")))})}if(aZ&&typeof aZ==="string"){var a0=(aZ||"").split(R);for(var aW=0,aV=this.length;aW<aV;aW++){var aY=this[aW];if(aY.nodeType===1){if(!aY.className){aY.className=aZ}else{var aX=" "+aY.className+" ";for(var a1=0,aU=a0.length;a1<aU;a1++){if(aX.indexOf(" "+a0[a1]+" ")<0){aY.className+=" "+a0[a1]}}}}}}return this},removeClass:function(aZ){if(a.isFunction(aZ)){return this.each(function(a3){var a2=a(this);a2.removeClass(aZ.call(this,a3,a2.attr("class")))})}if((aZ&&typeof aZ==="string")||aZ===B){var a0=(aZ||"").split(R);for(var aW=0,aV=this.length;aW<aV;aW++){var aY=this[aW];if(aY.nodeType===1&&aY.className){if(aZ){var aX=(" "+aY.className+" ").replace(am," ");for(var a1=0,aU=a0.length;a1<aU;a1++){aX=aX.replace(" "+a0[a1]+" "," ")}aY.className=aX.substring(1,aX.length-1)}else{aY.className=""}}}}return this},toggleClass:function(aX,aV){var aW=typeof aX,aU=typeof aV==="boolean";if(a.isFunction(aX)){return this.each(function(aZ){var aY=a(this);aY.toggleClass(aX.call(this,aZ,aY.attr("class"),aV),aV)})}return this.each(function(){if(aW==="string"){var a0,aZ=0,aY=a(this),a1=aV,a2=aX.split(R);while((a0=a2[aZ++])){a1=aU?a1:!aY.hasClass(a0);aY[a1?"addClass":"removeClass"](a0)}}else{if(aW==="undefined"||aW==="boolean"){if(this.className){a.data(this,"__className__",this.className)}this.className=this.className||aX===false?"":a.data(this,"__className__")||""}}})},hasClass:function(aU){var aX=" "+aU+" ";for(var aW=0,aV=this.length;aW<aV;aW++){if((" "+this[aW].className+" ").replace(am," ").indexOf(aX)>-1){return true}}return false},val:function(a1){if(a1===B){var aV=this[0];if(aV){if(a.nodeName(aV,"option")){return(aV.attributes.value||{}).specified?aV.value:aV.text}if(a.nodeName(aV,"select")){var aZ=aV.selectedIndex,a2=[],a3=aV.options,aY=aV.type==="select-one";if(aZ<0){return null}for(var aW=aY?aZ:0,a0=aY?aZ+1:a3.length;aW<a0;aW++){var aX=a3[aW];if(aX.selected){a1=a(aX).val();if(aY){return a1}a2.push(a1)}}return a2}if(G.test(aV.type)&&!a.support.checkOn){return aV.getAttribute("value")===null?"on":aV.value}return(aV.value||"").replace(at,"")}return B}var aU=a.isFunction(a1);return this.each(function(a6){var a5=a(this),a7=a1;if(this.nodeType!==1){return}if(aU){a7=a1.call(this,a6,a5.val())}if(typeof a7==="number"){a7+=""}if(a.isArray(a7)&&G.test(this.type)){this.checked=a.inArray(a5.val(),a7)>=0}else{if(a.nodeName(this,"select")){var a4=a.makeArray(a7);a("option",this).each(function(){this.selected=a.inArray(a(this).val(),a4)>=0});if(!a4.length){this.selectedIndex=-1}}else{this.value=a7}}})}});a.extend({attrFn:{val:true,css:true,html:true,text:true,data:true,width:true,height:true,offset:true},attr:function(aV,aU,a0,a3){if(!aV||aV.nodeType===3||aV.nodeType===8){return B}if(a3&&aU in a.attrFn){return a(aV)[aU](a0)}var aW=aV.nodeType!==1||!a.isXMLDoc(aV),aZ=a0!==B;aU=aW&&a.props[aU]||aU;if(aV.nodeType===1){var aY=aM.test(aU);if(aU==="selected"&&!a.support.optSelected){var a1=aV.parentNode;if(a1){a1.selectedIndex;if(a1.parentNode){a1.parentNode.selectedIndex}}}if(aU in aV&&aW&&!aY){if(aZ){if(aU==="type"&&d.test(aV.nodeName)&&aV.parentNode){a.error("type property can't be changed")}aV[aU]=a0}if(a.nodeName(aV,"form")&&aV.getAttributeNode(aU)){return aV.getAttributeNode(aU).nodeValue}if(aU==="tabIndex"){var a2=aV.getAttributeNode("tabIndex");return a2&&a2.specified?a2.value:y.test(aV.nodeName)||j.test(aV.nodeName)&&aV.href?0:B}return aV[aU]}if(!a.support.style&&aW&&aU==="style"){if(aZ){aV.style.cssText=""+a0}return aV.style.cssText}if(aZ){aV.setAttribute(aU,""+a0)}var aX=!a.support.hrefNormalized&&aW&&aY?aV.getAttribute(aU,2):aV.getAttribute(aU);return aX===null?B:aX}return a.style(aV,aU,a0)}});var z=function(aU){return aU.replace(/[^\w\s\.\|`]/g,function(aV){return"\\"+aV})};a.event={add:function(aW,a1,a6,aY){if(aW.nodeType===3||aW.nodeType===8){return}if(aW.setInterval&&(aW!==aI&&!aW.frameElement)){aW=aI}if(!a6.guid){a6.guid=a.guid++}if(aY!==B){var a4=a6;a6=a.proxy(a4);a6.data=aY}var a7=a.data(aW,"events")||a.data(aW,"events",{}),a0=a.data(aW,"handle"),aZ;if(!a0){aZ=function(){return typeof a!=="undefined"&&!a.event.triggered?a.event.handle.apply(aZ.elem,arguments):B};a0=a.data(aW,"handle",aZ)}if(!a0){return}a0.elem=aW;a1=a1.split(/\s+/);var a3,aX=0;while((a3=a1[aX++])){var aU=a3.split(".");a3=aU.shift();if(aX>1){a6=a.proxy(a6);if(aY!==B){a6.data=aY}}a6.type=aU.slice(0).sort().join(".");var aV=a7[a3],a2=this.special[a3]||{};if(!aV){aV=a7[a3]={};if(!a2.setup||a2.setup.call(aW,aY,aU,a6)===false){if(aW.addEventListener){aW.addEventListener(a3,a0,false)}else{if(aW.attachEvent){aW.attachEvent("on"+a3,a0)}}}}if(a2.add){var a5=a2.add.call(aW,a6,aY,aU,aV);if(a5&&a.isFunction(a5)){a5.guid=a5.guid||a6.guid;a5.data=a5.data||a6.data;a5.type=a5.type||a6.type;a6=a5}}aV[a6.guid]=a6;this.global[a3]=true}aW=null},global:{},remove:function(aW,a0,a6){if(aW.nodeType===3||aW.nodeType===8){return}var a7=a.data(aW,"events"),a1,a3,a4;if(a7){if(a0===B||(typeof a0==="string"&&a0.charAt(0)===".")){for(a3 in a7){this.remove(aW,a3+(a0||""))}}else{if(a0.type){a6=a0.handler;a0=a0.type}a0=a0.split(/\s+/);var aY=0;while((a3=a0[aY++])){var aU=a3.split(".");a3=aU.shift();var a5=!aU.length,aV=a.map(aU.slice(0).sort(),z),aX=new RegExp("(^|\\.)"+aV.join("\\.(?:.*\\.)?")+"(\\.|$)"),a2=this.special[a3]||{};if(a7[a3]){if(a6){a4=a7[a3][a6.guid];delete a7[a3][a6.guid]}else{for(var aZ in a7[a3]){if(a5||aX.test(a7[a3][aZ].type)){delete a7[a3][aZ]}}}if(a2.remove){a2.remove.call(aW,aU,a4)}for(a1 in a7[a3]){break}if(!a1){if(!a2.teardown||a2.teardown.call(aW,aU)===false){if(aW.removeEventListener){aW.removeEventListener(a3,a.data(aW,"handle"),false)}else{if(aW.detachEvent){aW.detachEvent("on"+a3,a.data(aW,"handle"))}}}a1=null;delete a7[a3]}}}}for(a1 in a7){break}if(!a1){var aZ=a.data(aW,"handle");if(aZ){aZ.elem=null}a.removeData(aW,"events");a.removeData(aW,"handle")}}},trigger:function(aU,aY,aW){var a2=aU.type||aU,aX=arguments[3];if(!aX){aU=typeof aU==="object"?aU[aE]?aU:a.extend(a.Event(a2),aU):a.Event(a2);if(a2.indexOf("!")>=0){aU.type=a2=a2.slice(0,-1);aU.exclusive=true}if(!aW){aU.stopPropagation();if(this.global[a2]){a.each(a.cache,function(){if(this.events&&this.events[a2]){a.event.trigger(aU,aY,this.handle.elem)}})}}if(!aW||aW.nodeType===3||aW.nodeType===8){return B}aU.result=B;aU.target=aW;aY=a.makeArray(aY);aY.unshift(aU)}aU.currentTarget=aW;var aZ=a.data(aW,"handle");if(aZ){aZ.apply(aW,aY)}var a3=aW.parentNode||aW.ownerDocument;try{if(!(aW&&aW.nodeName&&a.noData[aW.nodeName.toLowerCase()])){if(aW["on"+a2]&&aW["on"+a2].apply(aW,aY)===false){aU.result=false}}}catch(a1){}if(!aU.isPropagationStopped()&&a3){a.event.trigger(aU,aY,a3,true)}else{if(!aU.isDefaultPrevented()){var a0=aU.target,aV,a4=a.nodeName(a0,"a")&&a2==="click";if(!a4&&!(a0&&a0.nodeName&&a.noData[a0.nodeName.toLowerCase()])){try{if(a0[a2]){aV=a0["on"+a2];if(aV){a0["on"+a2]=null}this.triggered=true;a0[a2]()}}catch(a1){}if(aV){a0["on"+a2]=aV}this.triggered=false}}}},handle:function(a0){var aZ,aU;a0=arguments[0]=a.event.fix(a0||aI.event);a0.currentTarget=this;var a1=a0.type.split(".");a0.type=a1.shift();aZ=!a1.length&&!a0.exclusive;var aY=new RegExp("(^|\\.)"+a1.slice(0).sort().join("\\.(?:.*\\.)?")+"(\\.|$)");aU=(a.data(this,"events")||{})[a0.type];for(var aW in aU){var aX=aU[aW];if(aZ||aY.test(aX.type)){a0.handler=aX;a0.data=aX.data;var aV=aX.apply(this,arguments);if(aV!==B){a0.result=aV;if(aV===false){a0.preventDefault();a0.stopPropagation()}}if(a0.isImmediatePropagationStopped()){break}}}return a0.result},props:"altKey attrChange attrName bubbles button cancelable charCode clientX clientY ctrlKey currentTarget data detail eventPhase fromElement handler keyCode layerX layerY metaKey newValue offsetX offsetY originalTarget pageX pageY prevValue relatedNode relatedTarget screenX screenY shiftKey srcElement target toElement view wheelDelta which".split(" "),fix:function(aX){if(aX[aE]){return aX}var aV=aX;aX=a.Event(aV);for(var aW=this.props.length,aZ;aW;){aZ=this.props[--aW];aX[aZ]=aV[aZ]}if(!aX.target){aX.target=aX.srcElement||aa}if(aX.target.nodeType===3){aX.target=aX.target.parentNode}if(!aX.relatedTarget&&aX.fromElement){aX.relatedTarget=aX.fromElement===aX.target?aX.toElement:aX.fromElement}if(aX.pageX==null&&aX.clientX!=null){var aY=aa.documentElement,aU=aa.body;aX.pageX=aX.clientX+(aY&&aY.scrollLeft||aU&&aU.scrollLeft||0)-(aY&&aY.clientLeft||aU&&aU.clientLeft||0);aX.pageY=aX.clientY+(aY&&aY.scrollTop||aU&&aU.scrollTop||0)-(aY&&aY.clientTop||aU&&aU.clientTop||0)}if(!aX.which&&((aX.charCode||aX.charCode===0)?aX.charCode:aX.keyCode)){aX.which=aX.charCode||aX.keyCode}if(!aX.metaKey&&aX.ctrlKey){aX.metaKey=aX.ctrlKey}if(!aX.which&&aX.button!==B){aX.which=(aX.button&1?1:(aX.button&2?3:(aX.button&4?2:0)))}return aX},guid:100000000,proxy:a.proxy,special:{ready:{setup:a.bindReady,teardown:a.noop},live:{add:function(aU,aX,aW,aV){a.extend(aU,aX||{});aU.guid+=aX.selector+aX.live;aX.liveProxy=aU;a.event.add(this,aX.live,U,aX)},remove:function(aW){if(aW.length){var aU=0,aV=new RegExp("(^|\\.)"+aW[0]+"(\\.|$)");a.each((a.data(this,"events").live||{}),function(){if(aV.test(this.type)){aU++}});if(aU<1){a.event.remove(this,aW[0],U)}}},special:{}},beforeunload:{setup:function(aW,aV,aU){if(this.setInterval){this.onbeforeunload=aU}return false},teardown:function(aV,aU){if(this.onbeforeunload===aU){this.onbeforeunload=null}}}}};a.Event=function(aU){if(!this.preventDefault){return new a.Event(aU)}if(aU&&aU.type){this.originalEvent=aU;this.type=aU.type}else{this.type=aU}this.timeStamp=aL();this[aE]=true};function aN(){return false}function f(){return true}a.Event.prototype={preventDefault:function(){this.isDefaultPrevented=f;var aU=this.originalEvent;if(!aU){return}if(aU.preventDefault){aU.preventDefault()}aU.returnValue=false},stopPropagation:function(){this.isPropagationStopped=f;var aU=this.originalEvent;if(!aU){return}if(aU.stopPropagation){aU.stopPropagation()}aU.cancelBubble=true},stopImmediatePropagation:function(){this.isImmediatePropagationStopped=f;this.stopPropagation()},isDefaultPrevented:aN,isPropagationStopped:aN,isImmediatePropagationStopped:aN};var P=function(aV){var aU=aV.relatedTarget;while(aU&&aU!==this){try{aU=aU.parentNode}catch(aW){break}}if(aU!==this){aV.type=aV.data;a.event.handle.apply(this,arguments)}},av=function(aU){aU.type=aU.data;a.event.handle.apply(this,arguments)};a.each({mouseenter:"mouseover",mouseleave:"mouseout"},function(aV,aU){a.event.special[aV]={setup:function(aW){a.event.add(this,aU,aW&&aW.selector?av:P,aV)},teardown:function(aW){a.event.remove(this,aU,aW&&aW.selector?av:P)}}});if(!a.support.submitBubbles){a.event.special.submit={setup:function(aW,aV,aU){if(this.nodeName.toLowerCase()!=="form"){a.event.add(this,"click.specialSubmit."+aU.guid,function(aZ){var aY=aZ.target,aX=aY.type;if((aX==="submit"||aX==="image")&&a(aY).closest("form").length){return ax("submit",this,arguments)}});a.event.add(this,"keypress.specialSubmit."+aU.guid,function(aZ){var aY=aZ.target,aX=aY.type;if((aX==="text"||aX==="password")&&a(aY).closest("form").length&&aZ.keyCode===13){return ax("submit",this,arguments)}})}else{return false}},remove:function(aV,aU){a.event.remove(this,"click.specialSubmit"+(aU?"."+aU.guid:""));a.event.remove(this,"keypress.specialSubmit"+(aU?"."+aU.guid:""))}}}if(!a.support.changeBubbles){var ao=/textarea|input|select/i;function i(aV){var aU=aV.type,aW=aV.value;if(aU==="radio"||aU==="checkbox"){aW=aV.checked}else{if(aU==="select-multiple"){aW=aV.selectedIndex>-1?a.map(aV.options,function(aX){return aX.selected}).join("-"):""}else{if(aV.nodeName.toLowerCase()==="select"){aW=aV.selectedIndex}}}return aW}function N(aW){var aU=aW.target,aV,aX;if(!ao.test(aU.nodeName)||aU.readOnly){return}aV=a.data(aU,"_change_data");aX=i(aU);if(aW.type!=="focusout"||aU.type!=="radio"){a.data(aU,"_change_data",aX)}if(aV===B||aX===aV){return}if(aV!=null||aX){aW.type="change";return a.event.trigger(aW,arguments[1],aU)}}a.event.special.change={filters:{focusout:N,click:function(aW){var aV=aW.target,aU=aV.type;if(aU==="radio"||aU==="checkbox"||aV.nodeName.toLowerCase()==="select"){return N.call(this,aW)}},keydown:function(aW){var aV=aW.target,aU=aV.type;if((aW.keyCode===13&&aV.nodeName.toLowerCase()!=="textarea")||(aW.keyCode===32&&(aU==="checkbox"||aU==="radio"))||aU==="select-multiple"){return N.call(this,aW)}},beforeactivate:function(aV){var aU=aV.target;if(aU.nodeName.toLowerCase()==="input"&&aU.type==="radio"){a.data(aU,"_change_data",i(aU))}}},setup:function(aX,aW,aV){for(var aU in aO){a.event.add(this,aU+".specialChange."+aV.guid,aO[aU])}return ao.test(this.nodeName)},remove:function(aW,aV){for(var aU in aO){a.event.remove(this,aU+".specialChange"+(aV?"."+aV.guid:""),aO[aU])}return ao.test(this.nodeName)}};var aO=a.event.special.change.filters}function ax(aV,aW,aU){aU[0].type=aV;return a.event.handle.apply(aW,aU)}if(aa.addEventListener){a.each({focus:"focusin",blur:"focusout"},function(aW,aU){a.event.special[aU]={setup:function(){this.addEventListener(aW,aV,true)},teardown:function(){this.removeEventListener(aW,aV,true)}};function aV(aX){aX=a.event.fix(aX);aX.type=aU;return a.event.handle.call(this,aX)}})}a.each(["bind","one"],function(aV,aU){a.fn[aU]=function(aZ,a0,aY){if(typeof aZ==="object"){for(var aW in aZ){this[aU](aW,a0,aZ[aW],aY)}return this}if(a.isFunction(a0)){aY=a0;a0=B}var aX=aU==="one"?a.proxy(aY,function(a1){a(this).unbind(a1,aX);return aY.apply(this,arguments)}):aY;return aZ==="unload"&&aU!=="one"?this.one(aZ,a0,aY):this.each(function(){a.event.add(this,aZ,aX,a0)})}});a.fn.extend({unbind:function(aW,aV){if(typeof aW==="object"&&!aW.preventDefault){for(var aU in aW){this.unbind(aU,aW[aU])}return this}return this.each(function(){a.event.remove(this,aW,aV)})},trigger:function(aU,aV){return this.each(function(){a.event.trigger(aU,aV,this)})},triggerHandler:function(aU,aW){if(this[0]){var aV=a.Event(aU);aV.preventDefault();aV.stopPropagation();a.event.trigger(aV,aW,this[0]);return aV.result}},toggle:function(aW){var aU=arguments,aV=1;while(aV<aU.length){a.proxy(aW,aU[aV++])}return this.click(a.proxy(aW,function(aX){var aY=(a.data(this,"lastToggle"+aW.guid)||0)%aV;a.data(this,"lastToggle"+aW.guid,aY+1);aX.preventDefault();return aU[aY].apply(this,arguments)||false}))},hover:function(aU,aV){return this.mouseenter(aU).mouseleave(aV||aU)}});a.each(["live","die"],function(aV,aU){a.fn[aU]=function(aX,a0,aZ){var aY,aW=0;if(a.isFunction(a0)){aZ=a0;a0=B}aX=(aX||"").split(/\s+/);while((aY=aX[aW++])!=null){aY=aY==="focus"?"focusin":aY==="blur"?"focusout":aY==="hover"?aX.push("mouseleave")&&"mouseenter":aY;if(aU==="live"){a(this.context).bind(m(aY,this.selector),{data:a0,selector:this.selector,live:aY},aZ)}else{a(this.context).unbind(m(aY,this.selector),aZ?{guid:aZ.guid+this.selector+aY}:null)}}return this}});function U(aU){var a5,aV=[],a7=[],a3=arguments,a6,a2,a4,aX,aZ,a1,aY,a0,aW=a.extend({},a.data(this,"events").live);if(aU.button&&aU.type==="click"){return}for(aZ in aW){a4=aW[aZ];if(a4.live===aU.type||a4.altLive&&a.inArray(aU.type,a4.altLive)>-1){a0=a4.data;if(!(a0.beforeFilter&&a0.beforeFilter[aU.type]&&!a0.beforeFilter[aU.type](aU))){a7.push(a4.selector)}}else{delete aW[aZ]}}a2=a(aU.target).closest(a7,aU.currentTarget);for(a1=0,aY=a2.length;a1<aY;a1++){for(aZ in aW){a4=aW[aZ];aX=a2[a1].elem;a6=null;if(a2[a1].selector===a4.selector){if(a4.live==="mouseenter"||a4.live==="mouseleave"){a6=a(aU.relatedTarget).closest(a4.selector)[0]}if(!a6||a6!==aX){aV.push({elem:aX,fn:a4})}}}}for(a1=0,aY=aV.length;a1<aY;a1++){a2=aV[a1];aU.currentTarget=a2.elem;aU.data=a2.fn.data;if(a2.fn.apply(a2.elem,a3)===false){a5=false;break}}return a5}function m(aV,aU){return"live."+(aV?aV+".":"")+aU.replace(/\./g,"`").replace(/ /g,"&")}a.each(("blur focus focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup error").split(" "),function(aV,aU){a.fn[aU]=function(aW){return aW?this.bind(aU,aW):this.trigger(aU)};if(a.attrFn){a.attrFn[aU]=true}});if(aI.attachEvent&&!aI.addEventListener){aI.attachEvent("onunload",function(){for(var aV in a.cache){if(a.cache[aV].handle){try{a.event.remove(a.cache[aV].handle.elem)}catch(aU){}}}});
/*
 * Sizzle CSS Selector Engine - v1.0
 *  Copyright 2009, The Dojo Foundation
 *  Released under the MIT, BSD, and GPL Licenses.
 *  More information: http://sizzlejs.com/
 */
}(function(){var a5=/((?:\((?:\([^()]+\)|[^()]+)+\)|\[(?:\[[^[\]]*\]|['"][^'"]*['"]|[^[\]'"]+)+\]|\\.|[^ >+~,(\[\\]+)+|[>+~])(\s*,\s*)?((?:.|\r|\n)*)/g,a6=0,a8=Object.prototype.toString,a0=false,aZ=true;[0,0].sort(function(){aZ=false;return 0});var aW=function(bh,bc,bk,bl){bk=bk||[];var bn=bc=bc||aa;if(bc.nodeType!==1&&bc.nodeType!==9){return[]}if(!bh||typeof bh!=="string"){return bk}var bi=[],be,bp,bs,bd,bg=true,bf=aX(bc),bm=bh;while((a5.exec(""),be=a5.exec(bm))!==null){bm=be[3];bi.push(be[1]);if(be[2]){bd=be[3];break}}if(bi.length>1&&a1.exec(bh)){if(bi.length===2&&a2.relative[bi[0]]){bp=a9(bi[0]+bi[1],bc)}else{bp=a2.relative[bi[0]]?[bc]:aW(bi.shift(),bc);while(bi.length){bh=bi.shift();if(a2.relative[bh]){bh+=bi.shift()}bp=a9(bh,bp)}}}else{if(!bl&&bi.length>1&&bc.nodeType===9&&!bf&&a2.match.ID.test(bi[0])&&!a2.match.ID.test(bi[bi.length-1])){var bo=aW.find(bi.shift(),bc,bf);bc=bo.expr?aW.filter(bo.expr,bo.set)[0]:bo.set[0]}if(bc){var bo=bl?{expr:bi.pop(),set:a4(bl)}:aW.find(bi.pop(),bi.length===1&&(bi[0]==="~"||bi[0]==="+")&&bc.parentNode?bc.parentNode:bc,bf);bp=bo.expr?aW.filter(bo.expr,bo.set):bo.set;if(bi.length>0){bs=a4(bp)}else{bg=false}while(bi.length){var br=bi.pop(),bq=br;if(!a2.relative[br]){br=""}else{bq=bi.pop()}if(bq==null){bq=bc}a2.relative[br](bs,bq,bf)}}else{bs=bi=[]}}if(!bs){bs=bp}if(!bs){aW.error(br||bh)}if(a8.call(bs)==="[object Array]"){if(!bg){bk.push.apply(bk,bs)}else{if(bc&&bc.nodeType===1){for(var bj=0;bs[bj]!=null;bj++){if(bs[bj]&&(bs[bj]===true||bs[bj].nodeType===1&&a3(bc,bs[bj]))){bk.push(bp[bj])}}}else{for(var bj=0;bs[bj]!=null;bj++){if(bs[bj]&&bs[bj].nodeType===1){bk.push(bp[bj])}}}}}else{a4(bs,bk)}if(bd){aW(bd,bn,bk,bl);aW.uniqueSort(bk)}return bk};aW.uniqueSort=function(bd){if(a7){a0=aZ;bd.sort(a7);if(a0){for(var bc=1;bc<bd.length;bc++){if(bd[bc]===bd[bc-1]){bd.splice(bc--,1)}}}}return bd};aW.matches=function(bc,bd){return aW(bc,null,null,bd)};aW.find=function(bj,bc,bk){var bi,bg;if(!bj){return[]}for(var bf=0,be=a2.order.length;bf<be;bf++){var bh=a2.order[bf],bg;if((bg=a2.leftMatch[bh].exec(bj))){var bd=bg[1];bg.splice(1,1);if(bd.substr(bd.length-1)!=="\\"){bg[1]=(bg[1]||"").replace(/\\/g,"");bi=a2.find[bh](bg,bc,bk);if(bi!=null){bj=bj.replace(a2.match[bh],"");break}}}}if(!bi){bi=bc.getElementsByTagName("*")}return{set:bi,expr:bj}};aW.filter=function(bn,bm,bq,bg){var be=bn,bs=[],bk=bm,bi,bc,bj=bm&&bm[0]&&aX(bm[0]);while(bn&&bm.length){for(var bl in a2.filter){if((bi=a2.leftMatch[bl].exec(bn))!=null&&bi[2]){var bd=a2.filter[bl],br,bp,bf=bi[1];bc=false;bi.splice(1,1);if(bf.substr(bf.length-1)==="\\"){continue}if(bk===bs){bs=[]}if(a2.preFilter[bl]){bi=a2.preFilter[bl](bi,bk,bq,bs,bg,bj);if(!bi){bc=br=true}else{if(bi===true){continue}}}if(bi){for(var bh=0;(bp=bk[bh])!=null;bh++){if(bp){br=bd(bp,bi,bh,bk);var bo=bg^!!br;if(bq&&br!=null){if(bo){bc=true}else{bk[bh]=false}}else{if(bo){bs.push(bp);bc=true}}}}}if(br!==B){if(!bq){bk=bs}bn=bn.replace(a2.match[bl],"");if(!bc){return[]}break}}}if(bn===be){if(bc==null){aW.error(bn)}else{break}}be=bn}return bk};aW.error=function(bc){throw"Syntax error, unrecognized expression: "+bc};var a2=aW.selectors={order:["ID","NAME","TAG"],match:{ID:/#((?:[\w\u00c0-\uFFFF-]|\\.)+)/,CLASS:/\.((?:[\w\u00c0-\uFFFF-]|\\.)+)/,NAME:/\[name=['"]*((?:[\w\u00c0-\uFFFF-]|\\.)+)['"]*\]/,ATTR:/\[\s*((?:[\w\u00c0-\uFFFF-]|\\.)+)\s*(?:(\S?=)\s*(['"]*)(.*?)\3|)\s*\]/,TAG:/^((?:[\w\u00c0-\uFFFF\*-]|\\.)+)/,CHILD:/:(only|nth|last|first)-child(?:\((even|odd|[\dn+-]*)\))?/,POS:/:(nth|eq|gt|lt|first|last|even|odd)(?:\((\d*)\))?(?=[^-]|$)/,PSEUDO:/:((?:[\w\u00c0-\uFFFF-]|\\.)+)(?:\((['"]?)((?:\([^\)]+\)|[^\(\)]*)+)\2\))?/},leftMatch:{},attrMap:{"class":"className","for":"htmlFor"},attrHandle:{href:function(bc){return bc.getAttribute("href")}},relative:{"+":function(bi,bd){var bf=typeof bd==="string",bh=bf&&!/\W/.test(bd),bj=bf&&!bh;if(bh){bd=bd.toLowerCase()}for(var be=0,bc=bi.length,bg;be<bc;be++){if((bg=bi[be])){while((bg=bg.previousSibling)&&bg.nodeType!==1){}bi[be]=bj||bg&&bg.nodeName.toLowerCase()===bd?bg||false:bg===bd}}if(bj){aW.filter(bd,bi,true)}},">":function(bi,bd){var bg=typeof bd==="string";if(bg&&!/\W/.test(bd)){bd=bd.toLowerCase();for(var be=0,bc=bi.length;be<bc;be++){var bh=bi[be];if(bh){var bf=bh.parentNode;bi[be]=bf.nodeName.toLowerCase()===bd?bf:false}}}else{for(var be=0,bc=bi.length;be<bc;be++){var bh=bi[be];if(bh){bi[be]=bg?bh.parentNode:bh.parentNode===bd}}if(bg){aW.filter(bd,bi,true)}}},"":function(bf,bd,bh){var be=a6++,bc=ba;if(typeof bd==="string"&&!/\W/.test(bd)){var bg=bd=bd.toLowerCase();bc=aU}bc("parentNode",bd,be,bf,bg,bh)},"~":function(bf,bd,bh){var be=a6++,bc=ba;if(typeof bd==="string"&&!/\W/.test(bd)){var bg=bd=bd.toLowerCase();bc=aU}bc("previousSibling",bd,be,bf,bg,bh)}},find:{ID:function(bd,be,bf){if(typeof be.getElementById!=="undefined"&&!bf){var bc=be.getElementById(bd[1]);return bc?[bc]:[]}},NAME:function(be,bh){if(typeof bh.getElementsByName!=="undefined"){var bd=[],bg=bh.getElementsByName(be[1]);for(var bf=0,bc=bg.length;bf<bc;bf++){if(bg[bf].getAttribute("name")===be[1]){bd.push(bg[bf])}}return bd.length===0?null:bd}},TAG:function(bc,bd){return bd.getElementsByTagName(bc[1])}},preFilter:{CLASS:function(bf,bd,be,bc,bi,bj){bf=" "+bf[1].replace(/\\/g,"")+" ";if(bj){return bf}for(var bg=0,bh;(bh=bd[bg])!=null;bg++){if(bh){if(bi^(bh.className&&(" "+bh.className+" ").replace(/[\t\n]/g," ").indexOf(bf)>=0)){if(!be){bc.push(bh)}}else{if(be){bd[bg]=false}}}}return false},ID:function(bc){return bc[1].replace(/\\/g,"")},TAG:function(bd,bc){return bd[1].toLowerCase()},CHILD:function(bc){if(bc[1]==="nth"){var bd=/(-?)(\d*)n((?:\+|-)?\d*)/.exec(bc[2]==="even"&&"2n"||bc[2]==="odd"&&"2n+1"||!/\D/.test(bc[2])&&"0n+"+bc[2]||bc[2]);bc[2]=(bd[1]+(bd[2]||1))-0;bc[3]=bd[3]-0}bc[0]=a6++;return bc},ATTR:function(bg,bd,be,bc,bh,bi){var bf=bg[1].replace(/\\/g,"");if(!bi&&a2.attrMap[bf]){bg[1]=a2.attrMap[bf]}if(bg[2]==="~="){bg[4]=" "+bg[4]+" "}return bg},PSEUDO:function(bg,bd,be,bc,bh){if(bg[1]==="not"){if((a5.exec(bg[3])||"").length>1||/^\w/.test(bg[3])){bg[3]=aW(bg[3],null,null,bd)}else{var bf=aW.filter(bg[3],bd,be,true^bh);if(!be){bc.push.apply(bc,bf)}return false}}else{if(a2.match.POS.test(bg[0])||a2.match.CHILD.test(bg[0])){return true}}return bg},POS:function(bc){bc.unshift(true);return bc}},filters:{enabled:function(bc){return bc.disabled===false&&bc.type!=="hidden"},disabled:function(bc){return bc.disabled===true},checked:function(bc){return bc.checked===true},selected:function(bc){bc.parentNode.selectedIndex;return bc.selected===true},parent:function(bc){return !!bc.firstChild},empty:function(bc){return !bc.firstChild},has:function(be,bd,bc){return !!aW(bc[3],be).length},header:function(bc){return/h\d/i.test(bc.nodeName)},text:function(bc){return"text"===bc.type},radio:function(bc){return"radio"===bc.type},checkbox:function(bc){return"checkbox"===bc.type},file:function(bc){return"file"===bc.type},password:function(bc){return"password"===bc.type},submit:function(bc){return"submit"===bc.type},image:function(bc){return"image"===bc.type},reset:function(bc){return"reset"===bc.type},button:function(bc){return"button"===bc.type||bc.nodeName.toLowerCase()==="button"},input:function(bc){return/input|select|textarea|button/i.test(bc.nodeName)}},setFilters:{first:function(bd,bc){return bc===0},last:function(be,bd,bc,bf){return bd===bf.length-1},even:function(bd,bc){return bc%2===0},odd:function(bd,bc){return bc%2===1},lt:function(be,bd,bc){return bd<bc[3]-0},gt:function(be,bd,bc){return bd>bc[3]-0},nth:function(be,bd,bc){return bc[3]-0===bd},eq:function(be,bd,bc){return bc[3]-0===bd}},filter:{PSEUDO:function(bi,be,bf,bj){var bd=be[1],bg=a2.filters[bd];if(bg){return bg(bi,bf,be,bj)}else{if(bd==="contains"){return(bi.textContent||bi.innerText||aV([bi])||"").indexOf(be[3])>=0}else{if(bd==="not"){var bh=be[3];for(var bf=0,bc=bh.length;bf<bc;bf++){if(bh[bf]===bi){return false}}return true}else{aW.error("Syntax error, unrecognized expression: "+bd)}}}},CHILD:function(bc,bf){var bi=bf[1],bd=bc;switch(bi){case"only":case"first":while((bd=bd.previousSibling)){if(bd.nodeType===1){return false}}if(bi==="first"){return true}bd=bc;case"last":while((bd=bd.nextSibling)){if(bd.nodeType===1){return false}}return true;case"nth":var be=bf[2],bl=bf[3];if(be===1&&bl===0){return true}var bh=bf[0],bk=bc.parentNode;if(bk&&(bk.sizcache!==bh||!bc.nodeIndex)){var bg=0;for(bd=bk.firstChild;bd;bd=bd.nextSibling){if(bd.nodeType===1){bd.nodeIndex=++bg}}bk.sizcache=bh}var bj=bc.nodeIndex-bl;if(be===0){return bj===0}else{return(bj%be===0&&bj/be>=0)}}},ID:function(bd,bc){return bd.nodeType===1&&bd.getAttribute("id")===bc},TAG:function(bd,bc){return(bc==="*"&&bd.nodeType===1)||bd.nodeName.toLowerCase()===bc},CLASS:function(bd,bc){return(" "+(bd.className||bd.getAttribute("class"))+" ").indexOf(bc)>-1},ATTR:function(bh,bf){var be=bf[1],bc=a2.attrHandle[be]?a2.attrHandle[be](bh):bh[be]!=null?bh[be]:bh.getAttribute(be),bi=bc+"",bg=bf[2],bd=bf[4];return bc==null?bg==="!=":bg==="="?bi===bd:bg==="*="?bi.indexOf(bd)>=0:bg==="~="?(" "+bi+" ").indexOf(bd)>=0:!bd?bi&&bc!==false:bg==="!="?bi!==bd:bg==="^="?bi.indexOf(bd)===0:bg==="$="?bi.substr(bi.length-bd.length)===bd:bg==="|="?bi===bd||bi.substr(0,bd.length+1)===bd+"-":false},POS:function(bg,bd,be,bh){var bc=bd[2],bf=a2.setFilters[bc];if(bf){return bf(bg,be,bd,bh)}}}};var a1=a2.match.POS;for(var aY in a2.match){a2.match[aY]=new RegExp(a2.match[aY].source+/(?![^\[]*\])(?![^\(]*\))/.source);a2.leftMatch[aY]=new RegExp(/(^(?:.|\r|\n)*?)/.source+a2.match[aY].source.replace(/\\(\d+)/g,function(bd,bc){return"\\"+(bc-0+1)}))}var a4=function(bd,bc){bd=Array.prototype.slice.call(bd,0);if(bc){bc.push.apply(bc,bd);return bc}return bd};try{Array.prototype.slice.call(aa.documentElement.childNodes,0)}catch(bb){a4=function(bg,bf){var bd=bf||[];if(a8.call(bg)==="[object Array]"){Array.prototype.push.apply(bd,bg)}else{if(typeof bg.length==="number"){for(var be=0,bc=bg.length;be<bc;be++){bd.push(bg[be])}}else{for(var be=0;bg[be];be++){bd.push(bg[be])}}}return bd}}var a7;if(aa.documentElement.compareDocumentPosition){a7=function(bd,bc){if(!bd.compareDocumentPosition||!bc.compareDocumentPosition){if(bd==bc){a0=true}return bd.compareDocumentPosition?-1:1}var be=bd.compareDocumentPosition(bc)&4?-1:bd===bc?0:1;if(be===0){a0=true}return be}}else{if("sourceIndex" in aa.documentElement){a7=function(bd,bc){if(!bd.sourceIndex||!bc.sourceIndex){if(bd==bc){a0=true}return bd.sourceIndex?-1:1}var be=bd.sourceIndex-bc.sourceIndex;if(be===0){a0=true}return be}}else{if(aa.createRange){a7=function(bf,bd){if(!bf.ownerDocument||!bd.ownerDocument){if(bf==bd){a0=true}return bf.ownerDocument?-1:1}var be=bf.ownerDocument.createRange(),bc=bd.ownerDocument.createRange();be.setStart(bf,0);be.setEnd(bf,0);bc.setStart(bd,0);bc.setEnd(bd,0);var bg=be.compareBoundaryPoints(Range.START_TO_END,bc);if(bg===0){a0=true}return bg}}}}function aV(bc){var bd="",bf;for(var be=0;bc[be];be++){bf=bc[be];if(bf.nodeType===3||bf.nodeType===4){bd+=bf.nodeValue}else{if(bf.nodeType!==8){bd+=aV(bf.childNodes)}}}return bd}(function(){var bd=aa.createElement("div"),be="script"+(new Date).getTime();bd.innerHTML="<a name='"+be+"'/>";var bc=aa.documentElement;bc.insertBefore(bd,bc.firstChild);if(aa.getElementById(be)){a2.find.ID=function(bg,bh,bi){if(typeof bh.getElementById!=="undefined"&&!bi){var bf=bh.getElementById(bg[1]);return bf?bf.id===bg[1]||typeof bf.getAttributeNode!=="undefined"&&bf.getAttributeNode("id").nodeValue===bg[1]?[bf]:B:[]}};a2.filter.ID=function(bh,bf){var bg=typeof bh.getAttributeNode!=="undefined"&&bh.getAttributeNode("id");return bh.nodeType===1&&bg&&bg.nodeValue===bf}}bc.removeChild(bd);bc=bd=null})();(function(){var bc=aa.createElement("div");bc.appendChild(aa.createComment(""));if(bc.getElementsByTagName("*").length>0){a2.find.TAG=function(bd,bh){var bg=bh.getElementsByTagName(bd[1]);if(bd[1]==="*"){var bf=[];for(var be=0;bg[be];be++){if(bg[be].nodeType===1){bf.push(bg[be])}}bg=bf}return bg}}bc.innerHTML="<a href='#'></a>";if(bc.firstChild&&typeof bc.firstChild.getAttribute!=="undefined"&&bc.firstChild.getAttribute("href")!=="#"){a2.attrHandle.href=function(bd){return bd.getAttribute("href",2)}}bc=null})();if(aa.querySelectorAll){(function(){var bc=aW,be=aa.createElement("div");be.innerHTML="<p class='TEST'></p>";if(be.querySelectorAll&&be.querySelectorAll(".TEST").length===0){return}aW=function(bi,bh,bf,bg){bh=bh||aa;if(!bg&&bh.nodeType===9&&!aX(bh)){try{return a4(bh.querySelectorAll(bi),bf)}catch(bj){}}return bc(bi,bh,bf,bg)};for(var bd in bc){aW[bd]=bc[bd]}be=null})()}(function(){var bc=aa.createElement("div");bc.innerHTML="<div class='test e'></div><div class='test'></div>";if(!bc.getElementsByClassName||bc.getElementsByClassName("e").length===0){return}bc.lastChild.className="e";if(bc.getElementsByClassName("e").length===1){return}a2.order.splice(1,0,"CLASS");a2.find.CLASS=function(bd,be,bf){if(typeof be.getElementsByClassName!=="undefined"&&!bf){return be.getElementsByClassName(bd[1])}};bc=null})();function aU(bd,bi,bh,bl,bj,bk){for(var bf=0,be=bl.length;bf<be;bf++){var bc=bl[bf];if(bc){bc=bc[bd];var bg=false;while(bc){if(bc.sizcache===bh){bg=bl[bc.sizset];break}if(bc.nodeType===1&&!bk){bc.sizcache=bh;bc.sizset=bf}if(bc.nodeName.toLowerCase()===bi){bg=bc;break}bc=bc[bd]}bl[bf]=bg}}}function ba(bd,bi,bh,bl,bj,bk){for(var bf=0,be=bl.length;bf<be;bf++){var bc=bl[bf];if(bc){bc=bc[bd];var bg=false;while(bc){if(bc.sizcache===bh){bg=bl[bc.sizset];break}if(bc.nodeType===1){if(!bk){bc.sizcache=bh;bc.sizset=bf}if(typeof bi!=="string"){if(bc===bi){bg=true;break}}else{if(aW.filter(bi,[bc]).length>0){bg=bc;break}}}bc=bc[bd]}bl[bf]=bg}}}var a3=aa.compareDocumentPosition?function(bd,bc){return bd.compareDocumentPosition(bc)&16}:function(bd,bc){return bd!==bc&&(bd.contains?bd.contains(bc):true)};var aX=function(bc){var bd=(bc?bc.ownerDocument||bc:0).documentElement;return bd?bd.nodeName!=="HTML":false};var a9=function(bc,bj){var bf=[],bg="",bh,be=bj.nodeType?[bj]:bj;while((bh=a2.match.PSEUDO.exec(bc))){bg+=bh[0];bc=bc.replace(a2.match.PSEUDO,"")}bc=a2.relative[bc]?bc+"*":bc;for(var bi=0,bd=be.length;bi<bd;bi++){aW(bc,be[bi],bf)}return aW.filter(bg,bf)};a.find=aW;a.expr=aW.selectors;a.expr[":"]=a.expr.filters;a.unique=aW.uniqueSort;a.getText=aV;a.isXMLDoc=aX;a.contains=a3;return;aI.Sizzle=aW})();var M=/Until$/,X=/^(?:parents|prevUntil|prevAll)/,aH=/,/,D=Array.prototype.slice;var ag=function(aX,aW,aU){if(a.isFunction(aW)){return a.grep(aX,function(aZ,aY){return !!aW.call(aZ,aY,aZ)===aU})}else{if(aW.nodeType){return a.grep(aX,function(aZ,aY){return(aZ===aW)===aU})}else{if(typeof aW==="string"){var aV=a.grep(aX,function(aY){return aY.nodeType===1});if(aS.test(aW)){return a.filter(aW,aV,!aU)}else{aW=a.filter(aW,aV)}}}}return a.grep(aX,function(aZ,aY){return(a.inArray(aZ,aW)>=0)===aU})};a.fn.extend({find:function(aU){var aW=this.pushStack("","find",aU),aZ=0;for(var aX=0,aV=this.length;aX<aV;aX++){aZ=aW.length;a.find(aU,this[aX],aW);if(aX>0){for(var a0=aZ;a0<aW.length;a0++){for(var aY=0;aY<aZ;aY++){if(aW[aY]===aW[a0]){aW.splice(a0--,1);break}}}}}return aW},has:function(aV){var aU=a(aV);return this.filter(function(){for(var aX=0,aW=aU.length;aX<aW;aX++){if(a.contains(this,aU[aX])){return true}}})},not:function(aU){return this.pushStack(ag(this,aU,false),"not",aU)},filter:function(aU){return this.pushStack(ag(this,aU,true),"filter",aU)},is:function(aU){return !!aU&&a.filter(aU,this).length>0},closest:function(a3,aU){if(a.isArray(a3)){var a0=[],a2=this[0],aZ,aY={},aW;if(a2&&a3.length){for(var aX=0,aV=a3.length;aX<aV;aX++){aW=a3[aX];if(!aY[aW]){aY[aW]=a.expr.match.POS.test(aW)?a(aW,aU||this.context):aW}}while(a2&&a2.ownerDocument&&a2!==aU){for(aW in aY){aZ=aY[aW];if(aZ.jquery?aZ.index(a2)>-1:a(a2).is(aZ)){a0.push({selector:aW,elem:a2});delete aY[aW]}}a2=a2.parentNode}}return a0}var a1=a.expr.match.POS.test(a3)?a(a3,aU||this.context):null;return this.map(function(a4,a5){while(a5&&a5.ownerDocument&&a5!==aU){if(a1?a1.index(a5)>-1:a(a5).is(a3)){return a5}a5=a5.parentNode}return null})},index:function(aU){if(!aU||typeof aU==="string"){return a.inArray(this[0],aU?a(aU):this.parent().children())}return a.inArray(aU.jquery?aU[0]:aU,this)},add:function(aU,aV){var aX=typeof aU==="string"?a(aU,aV||this.context):a.makeArray(aU),aW=a.merge(this.get(),aX);return this.pushStack(x(aX[0])||x(aW[0])?aW:a.unique(aW))},andSelf:function(){return this.add(this.prevObject)}});function x(aU){return !aU||!aU.parentNode||aU.parentNode.nodeType===11}a.each({parent:function(aV){var aU=aV.parentNode;return aU&&aU.nodeType!==11?aU:null},parents:function(aU){return a.dir(aU,"parentNode")},parentsUntil:function(aV,aU,aW){return a.dir(aV,"parentNode",aW)},next:function(aU){return a.nth(aU,2,"nextSibling")},prev:function(aU){return a.nth(aU,2,"previousSibling")},nextAll:function(aU){return a.dir(aU,"nextSibling")},prevAll:function(aU){return a.dir(aU,"previousSibling")},nextUntil:function(aV,aU,aW){return a.dir(aV,"nextSibling",aW)},prevUntil:function(aV,aU,aW){return a.dir(aV,"previousSibling",aW)},siblings:function(aU){return a.sibling(aU.parentNode.firstChild,aU)},children:function(aU){return a.sibling(aU.firstChild)},contents:function(aU){return a.nodeName(aU,"iframe")?aU.contentDocument||aU.contentWindow.document:a.makeArray(aU.childNodes)}},function(aU,aV){a.fn[aU]=function(aY,aW){var aX=a.map(this,aV,aY);if(!M.test(aU)){aW=aY}if(aW&&typeof aW==="string"){aX=a.filter(aW,aX)}aX=this.length>1?a.unique(aX):aX;if((this.length>1||aH.test(aW))&&X.test(aU)){aX=aX.reverse()}return this.pushStack(aX,aU,D.call(arguments).join(","))}});a.extend({filter:function(aW,aU,aV){if(aV){aW=":not("+aW+")"}return a.find.matches(aW,aU)},dir:function(aW,aV,aY){var aU=[],aX=aW[aV];while(aX&&aX.nodeType!==9&&(aY===B||aX.nodeType!==1||!a(aX).is(aY))){if(aX.nodeType===1){aU.push(aX)}aX=aX[aV]}return aU},nth:function(aY,aU,aW,aX){aU=aU||1;var aV=0;for(;aY;aY=aY[aW]){if(aY.nodeType===1&&++aV===aU){break}}return aY},sibling:function(aW,aV){var aU=[];for(;aW;aW=aW.nextSibling){if(aW.nodeType===1&&aW!==aV){aU.push(aW)}}return aU}});var S=/ jQuery\d+="(?:\d+|null)"/g,Y=/^\s+/,F=/(<([\w:]+)[^>]*?)\/>/g,aj=/^(?:area|br|col|embed|hr|img|input|link|meta|param)$/i,c=/<([\w:]+)/,t=/<tbody/i,J=/<|&\w+;/,l=/checked\s*(?:[^=]|=\s*.checked.)/i,p=function(aV,aW,aU){return aj.test(aU)?aV:aW+"></"+aU+">"},ab={option:[1,"<select multiple='multiple'>","</select>"],legend:[1,"<fieldset>","</fieldset>"],thead:[1,"<table>","</table>"],tr:[2,"<table><tbody>","</tbody></table>"],td:[3,"<table><tbody><tr>","</tr></tbody></table>"],col:[2,"<table><tbody></tbody><colgroup>","</colgroup></table>"],area:[1,"<map>","</map>"],_default:[0,"",""]};ab.optgroup=ab.option;ab.tbody=ab.tfoot=ab.colgroup=ab.caption=ab.thead;ab.th=ab.td;if(!a.support.htmlSerialize){ab._default=[1,"div<div>","</div>"]}a.fn.extend({text:function(aU){if(a.isFunction(aU)){return this.each(function(aW){var aV=a(this);aV.text(aU.call(this,aW,aV.text()))})}if(typeof aU!=="object"&&aU!==B){return this.empty().append((this[0]&&this[0].ownerDocument||aa).createTextNode(aU))}return a.getText(this)},wrapAll:function(aU){if(a.isFunction(aU)){return this.each(function(aW){a(this).wrapAll(aU.call(this,aW))})}if(this[0]){var aV=a(aU,this[0].ownerDocument).eq(0).clone(true);if(this[0].parentNode){aV.insertBefore(this[0])}aV.map(function(){var aW=this;while(aW.firstChild&&aW.firstChild.nodeType===1){aW=aW.firstChild}return aW}).append(this)}return this},wrapInner:function(aU){if(a.isFunction(aU)){return this.each(function(aV){a(this).wrapInner(aU.call(this,aV))})}return this.each(function(){var aV=a(this),aW=aV.contents();if(aW.length){aW.wrapAll(aU)}else{aV.append(aU)}})},wrap:function(aU){return this.each(function(){a(this).wrapAll(aU)})},unwrap:function(){return this.parent().each(function(){if(!a.nodeName(this,"body")){a(this).replaceWith(this.childNodes)}}).end()},append:function(){return this.domManip(arguments,true,function(aU){if(this.nodeType===1){this.appendChild(aU)}})},prepend:function(){return this.domManip(arguments,true,function(aU){if(this.nodeType===1){this.insertBefore(aU,this.firstChild)}})},before:function(){if(this[0]&&this[0].parentNode){return this.domManip(arguments,false,function(aV){this.parentNode.insertBefore(aV,this)})}else{if(arguments.length){var aU=a(arguments[0]);aU.push.apply(aU,this.toArray());return this.pushStack(aU,"before",arguments)}}},after:function(){if(this[0]&&this[0].parentNode){return this.domManip(arguments,false,function(aV){this.parentNode.insertBefore(aV,this.nextSibling)})}else{if(arguments.length){var aU=this.pushStack(this,"after",arguments);aU.push.apply(aU,a(arguments[0]).toArray());return aU}}},clone:function(aV){var aU=this.map(function(){if(!a.support.noCloneEvent&&!a.isXMLDoc(this)){var aX=this.outerHTML,aW=this.ownerDocument;if(!aX){var aY=aW.createElement("div");aY.appendChild(this.cloneNode(true));aX=aY.innerHTML}return a.clean([aX.replace(S,"").replace(Y,"")],aW)[0]}else{return this.cloneNode(true)}});if(aV===true){q(this,aU);q(this.find("*"),aU.find("*"))}return aU},html:function(aW){if(aW===B){return this[0]&&this[0].nodeType===1?this[0].innerHTML.replace(S,""):null}else{if(typeof aW==="string"&&!/<script/i.test(aW)&&(a.support.leadingWhitespace||!Y.test(aW))&&!ab[(c.exec(aW)||["",""])[1].toLowerCase()]){aW=aW.replace(F,p);try{for(var aV=0,aU=this.length;aV<aU;aV++){if(this[aV].nodeType===1){a.cleanData(this[aV].getElementsByTagName("*"));this[aV].innerHTML=aW}}}catch(aX){this.empty().append(aW)}}else{if(a.isFunction(aW)){this.each(function(a0){var aZ=a(this),aY=aZ.html();aZ.empty().append(function(){return aW.call(this,a0,aY)})})}else{this.empty().append(aW)}}}return this},replaceWith:function(aU){if(this[0]&&this[0].parentNode){if(!a.isFunction(aU)){aU=a(aU).detach()}else{return this.each(function(aX){var aW=a(this),aV=aW.html();aW.replaceWith(aU.call(this,aX,aV))})}return this.each(function(){var aW=this.nextSibling,aV=this.parentNode;a(this).remove();if(aW){a(aW).before(aU)}else{a(aV).append(aU)}})}else{return this.pushStack(a(a.isFunction(aU)?aU():aU),"replaceWith",aU)}},detach:function(aU){return this.remove(aU,true)},domManip:function(aZ,a3,a2){var aW,aY,a1=aZ[0],aV=[];if(!a.support.checkClone&&arguments.length===3&&typeof a1==="string"&&l.test(a1)){return this.each(function(){a(this).domManip(aZ,a3,a2,true)})}if(a.isFunction(a1)){return this.each(function(a5){var a4=a(this);aZ[0]=a1.call(this,a5,a3?a4.html():B);a4.domManip(aZ,a3,a2)})}if(this[0]){if(aZ[0]&&aZ[0].parentNode&&aZ[0].parentNode.nodeType===11){aW={fragment:aZ[0].parentNode}}else{aW=H(aZ,this,aV)}aY=aW.fragment.firstChild;if(aY){a3=a3&&a.nodeName(aY,"tr");for(var aX=0,aU=this.length;aX<aU;aX++){a2.call(a3?a0(this[aX],aY):this[aX],aW.cacheable||this.length>1||aX>0?aW.fragment.cloneNode(true):aW.fragment)}}if(aV){a.each(aV,aR)}}return this;function a0(a4,a5){return a.nodeName(a4,"table")?(a4.getElementsByTagName("tbody")[0]||a4.appendChild(a4.ownerDocument.createElement("tbody"))):a4}}});function q(aW,aU){var aV=0;aU.each(function(){if(this.nodeName!==(aW[aV]&&aW[aV].nodeName)){return}var a1=a.data(aW[aV++]),a0=a.data(this,a1),aX=a1&&a1.events;if(aX){delete a0.handle;a0.events={};for(var aZ in aX){for(var aY in aX[aZ]){a.event.add(this,aZ,aX[aZ][aY],aX[aZ][aY].data)}}}})}function H(aZ,aX,aV){var aY,aU,aW,a0;if(aZ.length===1&&typeof aZ[0]==="string"&&aZ[0].length<512&&aZ[0].indexOf("<option")<0&&(a.support.checkClone||!l.test(aZ[0]))){aU=true;aW=a.fragments[aZ[0]];if(aW){if(aW!==1){aY=aW}}}if(!aY){a0=(aX&&aX[0]?aX[0].ownerDocument||aX[0]:aa);aY=a0.createDocumentFragment();a.clean(aZ,a0,aY,aV)}if(aU){a.fragments[aZ[0]]=aW?aY:1}return{fragment:aY,cacheable:aU}}a.fragments={};a.each({appendTo:"append",prependTo:"prepend",insertBefore:"before",insertAfter:"after",replaceAll:"replaceWith"},function(aU,aV){a.fn[aU]=function(aW){var aZ=[],a1=a(aW);for(var a0=0,aX=a1.length;a0<aX;a0++){var aY=(a0>0?this.clone(true):this).get();a.fn[aV].apply(a(a1[a0]),aY);aZ=aZ.concat(aY)}return this.pushStack(aZ,aU,a1.selector)}});a.each({remove:function(aU,aV){if(!aU||a.filter(aU,[this]).length){if(!aV&&this.nodeType===1){a.cleanData(this.getElementsByTagName("*"));a.cleanData([this])}if(this.parentNode){this.parentNode.removeChild(this)}}},empty:function(){if(this.nodeType===1){a.cleanData(this.getElementsByTagName("*"))}while(this.firstChild){this.removeChild(this.firstChild)}}},function(aU,aV){a.fn[aU]=function(){return this.each(aV,arguments)}});a.extend({clean:function(aV,aZ,aX,aU){aZ=aZ||aa;if(typeof aZ.createElement==="undefined"){aZ=aZ.ownerDocument||aZ[0]&&aZ[0].ownerDocument||aa}var aW=[];a.each(aV,function(a6,a3){if(typeof a3==="number"){a3+=""}if(!a3){return}if(typeof a3==="string"&&!J.test(a3)){a3=aZ.createTextNode(a3)}else{if(typeof a3==="string"){a3=a3.replace(F,p);var a8=(c.exec(a3)||["",""])[1].toLowerCase(),a2=ab[a8]||ab._default,a5=a2[0],a0=aZ.createElement("div");a0.innerHTML=a2[1]+a3+a2[2];while(a5--){a0=a0.lastChild}if(!a.support.tbody){var a1=t.test(a3),a7=a8==="table"&&!a1?a0.firstChild&&a0.firstChild.childNodes:a2[1]==="<table>"&&!a1?a0.childNodes:[];for(var a4=a7.length-1;a4>=0;--a4){if(a.nodeName(a7[a4],"tbody")&&!a7[a4].childNodes.length){a7[a4].parentNode.removeChild(a7[a4])}}}if(!a.support.leadingWhitespace&&Y.test(a3)){a0.insertBefore(aZ.createTextNode(Y.exec(a3)[0]),a0.firstChild)}a3=a.makeArray(a0.childNodes)}}if(a3.nodeType){aW.push(a3)}else{aW=a.merge(aW,a3)}});if(aX){for(var aY=0;aW[aY];aY++){if(aU&&a.nodeName(aW[aY],"script")&&(!aW[aY].type||aW[aY].type.toLowerCase()==="text/javascript")){aU.push(aW[aY].parentNode?aW[aY].parentNode.removeChild(aW[aY]):aW[aY])}else{if(aW[aY].nodeType===1){aW.splice.apply(aW,[aY+1,0].concat(a.makeArray(aW[aY].getElementsByTagName("script"))))}aX.appendChild(aW[aY])}}}return aW},cleanData:function(aU){for(var aV=0,aW,aX;(aW=aU[aV])!=null;aV++){a.event.remove(aW);a.removeData(aW)}}});var ap=/z-?index|font-?weight|opacity|zoom|line-?height/i,T=/alpha\([^)]*\)/,Z=/opacity=([^)]*)/,af=/float/i,aw=/-([a-z])/ig,v=/([A-Z])/g,aK=/^-?\d+(?:px)?$/i,aQ=/^-?\d/,aG={position:"absolute",visibility:"hidden",display:"block"},V=["Left","Right"],aA=["Top","Bottom"],ai=aa.defaultView&&aa.defaultView.getComputedStyle,aJ=a.support.cssFloat?"cssFloat":"styleFloat",k=function(aU,aV){return aV.toUpperCase()};a.fn.css=function(aU,aV){return al(this,aU,aV,true,function(aX,aW,aY){if(aY===B){return a.curCSS(aX,aW)}if(typeof aY==="number"&&!ap.test(aW)){aY+="px"}a.style(aX,aW,aY)})};a.extend({style:function(aY,aV,aZ){if(!aY||aY.nodeType===3||aY.nodeType===8){return B}if((aV==="width"||aV==="height")&&parseFloat(aZ)<0){aZ=B}var aX=aY.style||aY,a0=aZ!==B;if(!a.support.opacity&&aV==="opacity"){if(a0){aX.zoom=1;var aU=parseInt(aZ,10)+""==="NaN"?"":"alpha(opacity="+aZ*100+")";var aW=aX.filter||a.curCSS(aY,"filter")||"";aX.filter=T.test(aW)?aW.replace(T,aU):aU}return aX.filter&&aX.filter.indexOf("opacity=")>=0?(parseFloat(Z.exec(aX.filter)[1])/100)+"":""}if(af.test(aV)){aV=aJ}aV=aV.replace(aw,k);if(a0){aX[aV]=aZ}return aX[aV]},css:function(aX,aV,aZ,aU){if(aV==="width"||aV==="height"){var a1,aW=aG,a0=aV==="width"?V:aA;function aY(){a1=aV==="width"?aX.offsetWidth:aX.offsetHeight;if(aU==="border"){return}a.each(a0,function(){if(!aU){a1-=parseFloat(a.curCSS(aX,"padding"+this,true))||0}if(aU==="margin"){a1+=parseFloat(a.curCSS(aX,"margin"+this,true))||0}else{a1-=parseFloat(a.curCSS(aX,"border"+this+"Width",true))||0}})}if(aX.offsetWidth!==0){aY()}else{a.swap(aX,aW,aY)}return Math.max(0,Math.round(a1))}return a.curCSS(aX,aV,aZ)},curCSS:function(a0,aV,aW){var a3,aU=a0.style,aX;if(!a.support.opacity&&aV==="opacity"&&a0.currentStyle){a3=Z.test(a0.currentStyle.filter||"")?(parseFloat(RegExp.$1)/100)+"":"";return a3===""?"1":a3}if(af.test(aV)){aV=aJ}if(!aW&&aU&&aU[aV]){a3=aU[aV]}else{if(ai){if(af.test(aV)){aV="float"}aV=aV.replace(v,"-$1").toLowerCase();var a2=a0.ownerDocument.defaultView;if(!a2){return null}var a4=a2.getComputedStyle(a0,null);if(a4){a3=a4.getPropertyValue(aV)}if(aV==="opacity"&&a3===""){a3="1"}}else{if(a0.currentStyle){var aZ=aV.replace(aw,k);a3=a0.currentStyle[aV]||a0.currentStyle[aZ];if(!aK.test(a3)&&aQ.test(a3)){var aY=aU.left,a1=a0.runtimeStyle.left;a0.runtimeStyle.left=a0.currentStyle.left;aU.left=aZ==="fontSize"?"1em":(a3||0);a3=aU.pixelLeft+"px";aU.left=aY;a0.runtimeStyle.left=a1}}}}return a3},swap:function(aX,aW,aY){var aU={};for(var aV in aW){aU[aV]=aX.style[aV];aX.style[aV]=aW[aV]}aY.call(aX);for(var aV in aW){aX.style[aV]=aU[aV]}}});if(a.expr&&a.expr.filters){a.expr.filters.hidden=function(aX){var aV=aX.offsetWidth,aU=aX.offsetHeight,aW=aX.nodeName.toLowerCase()==="tr";return aV===0&&aU===0&&!aW?true:aV>0&&aU>0&&!aW?false:a.curCSS(aX,"display")==="none"};a.expr.filters.visible=function(aU){return !a.expr.filters.hidden(aU)}}var ae=aL(),aF=/<script(.|\s)*?\/script>/gi,o=/select|textarea/i,ay=/color|date|datetime|email|hidden|month|number|password|range|search|tel|text|time|url|week/i,r=/=\?(&|$)/,C=/\?/,aT=/(\?|&)_=.*?(&|$)/,A=/^(\w+:)?\/\/([^\/?#]+)/,h=/%20/g;a.fn.extend({_load:a.fn.load,load:function(aW,aZ,a0){if(typeof aW!=="string"){return this._load(aW)}else{if(!this.length){return this}}var aY=aW.indexOf(" ");if(aY>=0){var aU=aW.slice(aY,aW.length);aW=aW.slice(0,aY)}var aX="GET";if(aZ){if(a.isFunction(aZ)){a0=aZ;aZ=null}else{if(typeof aZ==="object"){aZ=a.param(aZ,a.ajaxSettings.traditional);aX="POST"}}}var aV=this;a.ajax({url:aW,type:aX,dataType:"html",data:aZ,complete:function(a2,a1){if(a1==="success"||a1==="notmodified"){aV.html(aU?a("<div />").append(a2.responseText.replace(aF,"")).find(aU):a2.responseText)}if(a0){aV.each(a0,[a2.responseText,a1,a2])}}});return this},serialize:function(){return a.param(this.serializeArray())},serializeArray:function(){return this.map(function(){return this.elements?a.makeArray(this.elements):this}).filter(function(){return this.name&&!this.disabled&&(this.checked||o.test(this.nodeName)||ay.test(this.type))}).map(function(aU,aV){var aW=a(this).val();return aW==null?null:a.isArray(aW)?a.map(aW,function(aY,aX){return{name:aV.name,value:aY}}):{name:aV.name,value:aW}}).get()}});a.each("ajaxStart ajaxStop ajaxComplete ajaxError ajaxSuccess ajaxSend".split(" "),function(aU,aV){a.fn[aV]=function(aW){return this.bind(aV,aW)}});a.extend({get:function(aU,aW,aX,aV){if(a.isFunction(aW)){aV=aV||aX;aX=aW;aW=null}return a.ajax({type:"GET",url:aU,data:aW,success:aX,dataType:aV})},getScript:function(aU,aV){return a.get(aU,null,aV,"script")},getJSON:function(aU,aV,aW){return a.get(aU,aV,aW,"json")},post:function(aU,aW,aX,aV){if(a.isFunction(aW)){aV=aV||aX;aX=aW;aW={}}return a.ajax({type:"POST",url:aU,data:aW,success:aX,dataType:aV})},ajaxSetup:function(aU){a.extend(a.ajaxSettings,aU)},ajaxSettings:{url:location.href,global:true,type:"GET",contentType:"application/x-www-form-urlencoded",processData:true,async:true,xhr:aI.XMLHttpRequest&&(aI.location.protocol!=="file:"||!aI.ActiveXObject)?function(){return new aI.XMLHttpRequest()}:function(){try{return new aI.ActiveXObject("Microsoft.XMLHTTP")}catch(aU){}},accepts:{xml:"application/xml, text/xml",html:"text/html",script:"text/javascript, application/javascript",json:"application/json, text/javascript",text:"text/plain",_default:"*/*"}},lastModified:{},etag:{},ajax:function(a9){var a4=a.extend(true,{},a.ajaxSettings,a9);var be,a8,bd,bf=a9&&a9.context||a4,aW=a4.type.toUpperCase();if(a4.data&&a4.processData&&typeof a4.data!=="string"){a4.data=a.param(a4.data,a4.traditional)}if(a4.dataType==="jsonp"){if(aW==="GET"){if(!r.test(a4.url)){a4.url+=(C.test(a4.url)?"&":"?")+(a4.jsonp||"callback")+"=?"}}else{if(!a4.data||!r.test(a4.data)){a4.data=(a4.data?a4.data+"&":"")+(a4.jsonp||"callback")+"=?"}}a4.dataType="json"}if(a4.dataType==="json"&&(a4.data&&r.test(a4.data)||r.test(a4.url))){be=a4.jsonpCallback||("jsonp"+ae++);if(a4.data){a4.data=(a4.data+"").replace(r,"="+be+"$1")}a4.url=a4.url.replace(r,"="+be+"$1");a4.dataType="script";aI[be]=aI[be]||function(bg){bd=bg;aZ();a2();aI[be]=B;try{delete aI[be]}catch(bh){}if(aX){aX.removeChild(bb)}}}if(a4.dataType==="script"&&a4.cache===null){a4.cache=false}if(a4.cache===false&&aW==="GET"){var aU=aL();var bc=a4.url.replace(aT,"$1_="+aU+"$2");a4.url=bc+((bc===a4.url)?(C.test(a4.url)?"&":"?")+"_="+aU:"")}if(a4.data&&aW==="GET"){a4.url+=(C.test(a4.url)?"&":"?")+a4.data}if(a4.global&&!a.active++){a.event.trigger("ajaxStart")}var a7=A.exec(a4.url),aY=a7&&(a7[1]&&a7[1]!==location.protocol||a7[2]!==location.host);if(a4.dataType==="script"&&aW==="GET"&&aY){var aX=aa.getElementsByTagName("head")[0]||aa.documentElement;var bb=aa.createElement("script");bb.src=a4.url;if(a4.scriptCharset){bb.charset=a4.scriptCharset}if(!be){var a6=false;bb.onload=bb.onreadystatechange=function(){if(!a6&&(!this.readyState||this.readyState==="loaded"||this.readyState==="complete")){a6=true;aZ();a2();bb.onload=bb.onreadystatechange=null;if(aX&&bb.parentNode){aX.removeChild(bb)}}}}aX.insertBefore(bb,aX.firstChild);return B}var a1=false;var a0=a4.xhr();if(!a0){return}if(a4.username){a0.open(aW,a4.url,a4.async,a4.username,a4.password)}else{a0.open(aW,a4.url,a4.async)}try{if(a4.data||a9&&a9.contentType){a0.setRequestHeader("Content-Type",a4.contentType)}if(a4.ifModified){if(a.lastModified[a4.url]){a0.setRequestHeader("If-Modified-Since",a.lastModified[a4.url])}if(a.etag[a4.url]){a0.setRequestHeader("If-None-Match",a.etag[a4.url])}}if(!aY){a0.setRequestHeader("X-Requested-With","XMLHttpRequest")}a0.setRequestHeader("Accept",a4.dataType&&a4.accepts[a4.dataType]?a4.accepts[a4.dataType]+", */*":a4.accepts._default)}catch(ba){}if(a4.beforeSend&&a4.beforeSend.call(bf,a0,a4)===false){if(a4.global&&!--a.active){a.event.trigger("ajaxStop")}a0.abort();return false}if(a4.global){a5("ajaxSend",[a0,a4])}var a3=a0.onreadystatechange=function(bg){if(!a0||a0.readyState===0||bg==="abort"){if(!a1){a2()}a1=true;if(a0){a0.onreadystatechange=a.noop}}else{if(!a1&&a0&&(a0.readyState===4||bg==="timeout")){a1=true;a0.onreadystatechange=a.noop;a8=bg==="timeout"?"timeout":!a.httpSuccess(a0)?"error":a4.ifModified&&a.httpNotModified(a0,a4.url)?"notmodified":"success";var bi;if(a8==="success"){try{bd=a.httpData(a0,a4.dataType,a4)}catch(bh){a8="parsererror";bi=bh}}if(a8==="success"||a8==="notmodified"){if(!be){aZ()}}else{a.handleError(a4,a0,a8,bi)}a2();if(bg==="timeout"){a0.abort()}if(a4.async){a0=null}}}};try{var aV=a0.abort;a0.abort=function(){if(a0){aV.call(a0)}a3("abort")}}catch(ba){}if(a4.async&&a4.timeout>0){setTimeout(function(){if(a0&&!a1){a3("timeout")}},a4.timeout)}try{a0.send(aW==="POST"||aW==="PUT"||aW==="DELETE"?a4.data:null)}catch(ba){a.handleError(a4,a0,null,ba);a2()}if(!a4.async){a3()}function aZ(){if(a4.success){a4.success.call(bf,bd,a8,a0)}if(a4.global){a5("ajaxSuccess",[a0,a4])}}function a2(){if(a4.complete){a4.complete.call(bf,a0,a8)}if(a4.global){a5("ajaxComplete",[a0,a4])}if(a4.global&&!--a.active){a.event.trigger("ajaxStop")}}function a5(bh,bg){(a4.context?a(a4.context):a.event).trigger(bh,bg)}return a0},handleError:function(aV,aX,aU,aW){if(aV.error){aV.error.call(aV.context||aV,aX,aU,aW)}if(aV.global){(aV.context?a(aV.context):a.event).trigger("ajaxError",[aX,aV,aW])}},active:0,httpSuccess:function(aV){try{return !aV.status&&location.protocol==="file:"||(aV.status>=200&&aV.status<300)||aV.status===304||aV.status===1223||aV.status===0}catch(aU){}return false},httpNotModified:function(aX,aU){var aW=aX.getResponseHeader("Last-Modified"),aV=aX.getResponseHeader("Etag");if(aW){a.lastModified[aU]=aW}if(aV){a.etag[aU]=aV}return aX.status===304||aX.status===0},httpData:function(aZ,aX,aW){var aV=aZ.getResponseHeader("content-type")||"",aU=aX==="xml"||!aX&&aV.indexOf("xml")>=0,aY=aU?aZ.responseXML:aZ.responseText;if(aU&&aY.documentElement.nodeName==="parsererror"){a.error("parsererror")}if(aW&&aW.dataFilter){aY=aW.dataFilter(aY,aX)}if(typeof aY==="string"){if(aX==="json"||!aX&&aV.indexOf("json")>=0){aY=a.parseJSON(aY)}else{if(aX==="script"||!aX&&aV.indexOf("javascript")>=0){a.globalEval(aY)}}}return aY},param:function(aU,aX){var aV=[];if(aX===B){aX=a.ajaxSettings.traditional}if(a.isArray(aU)||aU.jquery){a.each(aU,function(){aZ(this.name,this.value)})}else{for(var aY in aU){aW(aY,aU[aY])}}return aV.join("&").replace(h,"+");function aW(a0,a1){if(a.isArray(a1)){a.each(a1,function(a3,a2){if(aX){aZ(a0,a2)}else{aW(a0+"["+(typeof a2==="object"||a.isArray(a2)?a3:"")+"]",a2)}})}else{if(!aX&&a1!=null&&typeof a1==="object"){a.each(a1,function(a3,a2){aW(a0+"["+a3+"]",a2)})}else{aZ(a0,a1)}}}function aZ(a0,a1){a1=a.isFunction(a1)?a1():a1;aV[aV.length]=encodeURIComponent(a0)+"="+encodeURIComponent(a1)}}});var E={},ad=/toggle|show|hide/,ar=/^([+-]=)?([\d+-.]+)(.*)$/,aB,ah=[["height","marginTop","marginBottom","paddingTop","paddingBottom"],["width","marginLeft","marginRight","paddingLeft","paddingRight"],["opacity"]];a.fn.extend({show:function(aV,a3){if(aV||aV===0){return this.animate(az("show",3),aV,a3)}else{for(var a0=0,aX=this.length;a0<aX;a0++){var aU=a.data(this[a0],"olddisplay");this[a0].style.display=aU||"";if(a.css(this[a0],"display")==="none"){var a2=this[a0].nodeName,a1;if(E[a2]){a1=E[a2]}else{var aW=a("<"+a2+" />").appendTo("body");a1=aW.css("display");if(a1==="none"){a1="block"}aW.remove();E[a2]=a1}a.data(this[a0],"olddisplay",a1)}}for(var aZ=0,aY=this.length;aZ<aY;aZ++){this[aZ].style.display=a.data(this[aZ],"olddisplay")||""}return this}},hide:function(aZ,a0){if(aZ||aZ===0){return this.animate(az("hide",3),aZ,a0)}else{for(var aY=0,aV=this.length;aY<aV;aY++){var aU=a.data(this[aY],"olddisplay");if(!aU&&aU!=="none"){a.data(this[aY],"olddisplay",a.css(this[aY],"display"))}}for(var aX=0,aW=this.length;aX<aW;aX++){this[aX].style.display="none"}return this}},_toggle:a.fn.toggle,toggle:function(aW,aV){var aU=typeof aW==="boolean";if(a.isFunction(aW)&&a.isFunction(aV)){this._toggle.apply(this,arguments)}else{if(aW==null||aU){this.each(function(){var aX=aU?aW:a(this).is(":hidden");a(this)[aX?"show":"hide"]()})}else{this.animate(az("toggle",3),aW,aV)}}return this},fadeTo:function(aU,aW,aV){return this.filter(":hidden").css("opacity",0).show().end().animate({opacity:aW},aU,aV)},animate:function(aY,aV,aX,aW){var aU=a.speed(aV,aX,aW);if(a.isEmptyObject(aY)){return this.each(aU.complete)}return this[aU.queue===false?"each":"queue"](function(){var a1=a.extend({},aU),a3,a2=this.nodeType===1&&a(this).is(":hidden"),aZ=this;for(a3 in aY){var a0=a3.replace(aw,k);if(a3!==a0){aY[a0]=aY[a3];delete aY[a3];a3=a0}if(aY[a3]==="hide"&&a2||aY[a3]==="show"&&!a2){return a1.complete.call(this)}if((a3==="height"||a3==="width")&&this.style){a1.display=a.css(this,"display");a1.overflow=this.style.overflow}if(a.isArray(aY[a3])){(a1.specialEasing=a1.specialEasing||{})[a3]=aY[a3][1];aY[a3]=aY[a3][0]}}if(a1.overflow!=null){this.style.overflow="hidden"}a1.curAnim=a.extend({},aY);a.each(aY,function(a5,a9){var a8=new a.fx(aZ,a1,a5);if(ad.test(a9)){a8[a9==="toggle"?a2?"show":"hide":a9](aY)}else{var a7=ar.exec(a9),ba=a8.cur(true)||0;if(a7){var a4=parseFloat(a7[2]),a6=a7[3]||"px";if(a6!=="px"){aZ.style[a5]=(a4||1)+a6;ba=((a4||1)/a8.cur(true))*ba;aZ.style[a5]=ba+a6}if(a7[1]){a4=((a7[1]==="-="?-1:1)*a4)+ba}a8.custom(ba,a4,a6)}else{a8.custom(ba,a9,"")}}});return true})},stop:function(aV,aU){var aW=a.timers;if(aV){this.queue([])}this.each(function(){for(var aX=aW.length-1;aX>=0;aX--){if(aW[aX].elem===this){if(aU){aW[aX](true)}aW.splice(aX,1)}}});if(!aU){this.dequeue()}return this}});a.each({slideDown:az("show",1),slideUp:az("hide",1),slideToggle:az("toggle",1),fadeIn:{opacity:"show"},fadeOut:{opacity:"hide"}},function(aU,aV){a.fn[aU]=function(aW,aX){return this.animate(aV,aW,aX)}});a.extend({speed:function(aW,aX,aV){var aU=aW&&typeof aW==="object"?aW:{complete:aV||!aV&&aX||a.isFunction(aW)&&aW,duration:aW,easing:aV&&aX||aX&&!a.isFunction(aX)&&aX};aU.duration=a.fx.off?0:typeof aU.duration==="number"?aU.duration:a.fx.speeds[aU.duration]||a.fx.speeds._default;aU.old=aU.complete;aU.complete=function(){if(aU.queue!==false){a(this).dequeue()}if(a.isFunction(aU.old)){aU.old.call(this)}};return aU},easing:{linear:function(aW,aX,aU,aV){return aU+aV*aW},swing:function(aW,aX,aU,aV){return((-Math.cos(aW*Math.PI)/2)+0.5)*aV+aU}},timers:[],fx:function(aV,aU,aW){this.options=aU;this.elem=aV;this.prop=aW;if(!aU.orig){aU.orig={}}}});a.fx.prototype={update:function(){if(this.options.step){this.options.step.call(this.elem,this.now,this)}(a.fx.step[this.prop]||a.fx.step._default)(this);if((this.prop==="height"||this.prop==="width")&&this.elem.style){this.elem.style.display="block"}},cur:function(aV){if(this.elem[this.prop]!=null&&(!this.elem.style||this.elem.style[this.prop]==null)){return this.elem[this.prop]}var aU=parseFloat(a.css(this.elem,this.prop,aV));return aU&&aU>-10000?aU:parseFloat(a.curCSS(this.elem,this.prop))||0},custom:function(aY,aX,aW){this.startTime=aL();this.start=aY;this.end=aX;this.unit=aW||this.unit||"px";this.now=this.start;this.pos=this.state=0;var aU=this;function aV(aZ){return aU.step(aZ)}aV.elem=this.elem;if(aV()&&a.timers.push(aV)&&!aB){aB=setInterval(a.fx.tick,13)}},show:function(){this.options.orig[this.prop]=a.style(this.elem,this.prop);this.options.show=true;this.custom(this.prop==="width"||this.prop==="height"?1:0,this.cur());a(this.elem).show()},hide:function(){this.options.orig[this.prop]=a.style(this.elem,this.prop);this.options.hide=true;this.custom(this.cur(),0)},step:function(aX){var a2=aL(),aY=true;if(aX||a2>=this.options.duration+this.startTime){this.now=this.end;this.pos=this.state=1;this.update();this.options.curAnim[this.prop]=true;for(var aZ in this.options.curAnim){if(this.options.curAnim[aZ]!==true){aY=false}}if(aY){if(this.options.display!=null){this.elem.style.overflow=this.options.overflow;var aW=a.data(this.elem,"olddisplay");this.elem.style.display=aW?aW:this.options.display;if(a.css(this.elem,"display")==="none"){this.elem.style.display="block"}}if(this.options.hide){a(this.elem).hide()}if(this.options.hide||this.options.show){for(var aU in this.options.curAnim){a.style(this.elem,aU,this.options.orig[aU])}}this.options.complete.call(this.elem)}return false}else{var aV=a2-this.startTime;this.state=aV/this.options.duration;var a0=this.options.specialEasing&&this.options.specialEasing[this.prop];var a1=this.options.easing||(a.easing.swing?"swing":"linear");this.pos=a.easing[a0||a1](this.state,aV,0,1,this.options.duration);this.now=this.start+((this.end-this.start)*this.pos);this.update()}return true}};a.extend(a.fx,{tick:function(){var aV=a.timers;for(var aU=0;aU<aV.length;aU++){if(!aV[aU]()){aV.splice(aU--,1)}}if(!aV.length){a.fx.stop()}},stop:function(){clearInterval(aB);aB=null},speeds:{slow:600,fast:200,_default:400},step:{opacity:function(aU){a.style(aU.elem,"opacity",aU.now)},_default:function(aU){if(aU.elem.style&&aU.elem.style[aU.prop]!=null){aU.elem.style[aU.prop]=(aU.prop==="width"||aU.prop==="height"?Math.max(0,aU.now):aU.now)+aU.unit}else{aU.elem[aU.prop]=aU.now}}}});if(a.expr&&a.expr.filters){a.expr.filters.animated=function(aU){return a.grep(a.timers,function(aV){return aU===aV.elem}).length}}function az(aV,aU){var aW={};a.each(ah.concat.apply([],ah.slice(0,aU)),function(){aW[this]=aV});return aW}if("getBoundingClientRect" in aa.documentElement){a.fn.offset=function(a3){var aW=this[0];if(a3){return this.each(function(a4){a.offset.setOffset(this,a3,a4)})}if(!aW||!aW.ownerDocument){return null}if(aW===aW.ownerDocument.body){return a.offset.bodyOffset(aW)}var aY=aW.getBoundingClientRect(),a2=aW.ownerDocument,aZ=a2.body,aU=a2.documentElement,aX=aU.clientTop||aZ.clientTop||0,a0=aU.clientLeft||aZ.clientLeft||0,a1=aY.top+(self.pageYOffset||a.support.boxModel&&aU.scrollTop||aZ.scrollTop)-aX,aV=aY.left+(self.pageXOffset||a.support.boxModel&&aU.scrollLeft||aZ.scrollLeft)-a0;return{top:a1,left:aV}}}else{a.fn.offset=function(a5){var aZ=this[0];if(a5){return this.each(function(a6){a.offset.setOffset(this,a5,a6)})}if(!aZ||!aZ.ownerDocument){return null}if(aZ===aZ.ownerDocument.body){return a.offset.bodyOffset(aZ)}a.offset.initialize();var aW=aZ.offsetParent,aV=aZ,a4=aZ.ownerDocument,a2,aX=a4.documentElement,a0=a4.body,a1=a4.defaultView,aU=a1?a1.getComputedStyle(aZ,null):aZ.currentStyle,a3=aZ.offsetTop,aY=aZ.offsetLeft;while((aZ=aZ.parentNode)&&aZ!==a0&&aZ!==aX){if(a.offset.supportsFixedPosition&&aU.position==="fixed"){break}a2=a1?a1.getComputedStyle(aZ,null):aZ.currentStyle;a3-=aZ.scrollTop;aY-=aZ.scrollLeft;if(aZ===aW){a3+=aZ.offsetTop;aY+=aZ.offsetLeft;if(a.offset.doesNotAddBorder&&!(a.offset.doesAddBorderForTableAndCells&&/^t(able|d|h)$/i.test(aZ.nodeName))){a3+=parseFloat(a2.borderTopWidth)||0;aY+=parseFloat(a2.borderLeftWidth)||0}aV=aW,aW=aZ.offsetParent}if(a.offset.subtractsBorderForOverflowNotVisible&&a2.overflow!=="visible"){a3+=parseFloat(a2.borderTopWidth)||0;aY+=parseFloat(a2.borderLeftWidth)||0}aU=a2}if(aU.position==="relative"||aU.position==="static"){a3+=a0.offsetTop;aY+=a0.offsetLeft}if(a.offset.supportsFixedPosition&&aU.position==="fixed"){a3+=Math.max(aX.scrollTop,a0.scrollTop);aY+=Math.max(aX.scrollLeft,a0.scrollLeft)}return{top:a3,left:aY}}}a.offset={initialize:function(){var aU=aa.body,aV=aa.createElement("div"),aY,a0,aZ,a1,aW=parseFloat(a.curCSS(aU,"marginTop",true))||0,aX="<div style='position:absolute;top:0;left:0;margin:0;border:5px solid #000;padding:0;width:1px;height:1px;'><div></div></div><table style='position:absolute;top:0;left:0;margin:0;border:5px solid #000;padding:0;width:1px;height:1px;' cellpadding='0' cellspacing='0'><tr><td></td></tr></table>";a.extend(aV.style,{position:"absolute",top:0,left:0,margin:0,border:0,width:"1px",height:"1px",visibility:"hidden"});aV.innerHTML=aX;aU.insertBefore(aV,aU.firstChild);aY=aV.firstChild;a0=aY.firstChild;a1=aY.nextSibling.firstChild.firstChild;this.doesNotAddBorder=(a0.offsetTop!==5);this.doesAddBorderForTableAndCells=(a1.offsetTop===5);a0.style.position="fixed",a0.style.top="20px";this.supportsFixedPosition=(a0.offsetTop===20||a0.offsetTop===15);a0.style.position=a0.style.top="";aY.style.overflow="hidden",aY.style.position="relative";this.subtractsBorderForOverflowNotVisible=(a0.offsetTop===-5);this.doesNotIncludeMarginInBodyOffset=(aU.offsetTop!==aW);aU.removeChild(aV);aU=aV=aY=a0=aZ=a1=null;a.offset.initialize=a.noop},bodyOffset:function(aU){var aW=aU.offsetTop,aV=aU.offsetLeft;a.offset.initialize();if(a.offset.doesNotIncludeMarginInBodyOffset){aW+=parseFloat(a.curCSS(aU,"marginTop",true))||0;aV+=parseFloat(a.curCSS(aU,"marginLeft",true))||0}return{top:aW,left:aV}},setOffset:function(aZ,aV,aW){if(/static/.test(a.curCSS(aZ,"position"))){aZ.style.position="relative"}var aY=a(aZ),a1=aY.offset(),aU=parseInt(a.curCSS(aZ,"top",true),10)||0,a0=parseInt(a.curCSS(aZ,"left",true),10)||0;if(a.isFunction(aV)){aV=aV.call(aZ,aW,a1)}var aX={top:(aV.top-a1.top)+aU,left:(aV.left-a1.left)+a0};if("using" in aV){aV.using.call(aZ,aX)}else{aY.css(aX)}}};a.fn.extend({position:function(){if(!this[0]){return null}var aW=this[0],aV=this.offsetParent(),aX=this.offset(),aU=/^body|html$/i.test(aV[0].nodeName)?{top:0,left:0}:aV.offset();aX.top-=parseFloat(a.curCSS(aW,"marginTop",true))||0;aX.left-=parseFloat(a.curCSS(aW,"marginLeft",true))||0;aU.top+=parseFloat(a.curCSS(aV[0],"borderTopWidth",true))||0;aU.left+=parseFloat(a.curCSS(aV[0],"borderLeftWidth",true))||0;return{top:aX.top-aU.top,left:aX.left-aU.left}},offsetParent:function(){return this.map(function(){var aU=this.offsetParent||aa.body;while(aU&&(!/^body|html$/i.test(aU.nodeName)&&a.css(aU,"position")==="static")){aU=aU.offsetParent}return aU})}});a.each(["Left","Top"],function(aV,aU){var aW="scroll"+aU;a.fn[aW]=function(aZ){var aX=this[0],aY;if(!aX){return null}if(aZ!==B){return this.each(function(){aY=ak(this);if(aY){aY.scrollTo(!aV?aZ:a(aY).scrollLeft(),aV?aZ:a(aY).scrollTop())}else{this[aW]=aZ}})}else{aY=ak(aX);return aY?("pageXOffset" in aY)?aY[aV?"pageYOffset":"pageXOffset"]:a.support.boxModel&&aY.document.documentElement[aW]||aY.document.body[aW]:aX[aW]}}});function ak(aU){return("scrollTo" in aU&&aU.document)?aU:aU.nodeType===9?aU.defaultView||aU.parentWindow:false}a.each(["Height","Width"],function(aV,aU){var aW=aU.toLowerCase();a.fn["inner"+aU]=function(){return this[0]?a.css(this[0],aW,false,"padding"):null};a.fn["outer"+aU]=function(aX){return this[0]?a.css(this[0],aW,false,aX?"margin":"border"):null};a.fn[aW]=function(aX){var aY=this[0];if(!aY){return aX==null?null:this}if(a.isFunction(aX)){return this.each(function(a0){var aZ=a(this);aZ[aW](aX.call(this,a0,aZ[aW]()))})}return("scrollTo" in aY&&aY.document)?aY.document.compatMode==="CSS1Compat"&&aY.document.documentElement["client"+aU]||aY.document.body["client"+aU]:(aY.nodeType===9)?Math.max(aY.documentElement["client"+aU],aY.body["scroll"+aU],aY.documentElement["scroll"+aU],aY.body["offset"+aU],aY.documentElement["offset"+aU]):aX===B?a.css(aY,aW):this.css(aW,typeof aX==="string"?aX:aX+"px")}});aI.jQuery=aI.$=a})(window);
/*
 * jQuery UI 1.7.2
 *
 * Copyright (c) 2009 AUTHORS.txt (http://jqueryui.com/about)
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI
 */
jQuery.ui||(function(c){var i=c.fn.remove,d=c.browser.mozilla&&(parseFloat(c.browser.version)<1.9);c.ui={version:"1.7.2",plugin:{add:function(k,l,n){var m=c.ui[k].prototype;for(var j in n){m.plugins[j]=m.plugins[j]||[];m.plugins[j].push([l,n[j]])}},call:function(j,l,k){var n=j.plugins[l];if(!n||!j.element[0].parentNode){return}for(var m=0;m<n.length;m++){if(j.options[n[m][0]]){n[m][1].apply(j.element,k)}}}},contains:function(k,j){return document.compareDocumentPosition?k.compareDocumentPosition(j)&16:k!==j&&k.contains(j)},hasScroll:function(m,k){if(c(m).css("overflow")=="hidden"){return false}var j=(k&&k=="left")?"scrollLeft":"scrollTop",l=false;if(m[j]>0){return true}m[j]=1;l=(m[j]>0);m[j]=0;return l},isOverAxis:function(k,j,l){return(k>j)&&(k<(j+l))},isOver:function(o,k,n,m,j,l){return c.ui.isOverAxis(o,n,j)&&c.ui.isOverAxis(k,m,l)},keyCode:{BACKSPACE:8,CAPS_LOCK:20,COMMA:188,CONTROL:17,DELETE:46,DOWN:40,END:35,ENTER:13,ESCAPE:27,HOME:36,INSERT:45,LEFT:37,NUMPAD_ADD:107,NUMPAD_DECIMAL:110,NUMPAD_DIVIDE:111,NUMPAD_ENTER:108,NUMPAD_MULTIPLY:106,NUMPAD_SUBTRACT:109,PAGE_DOWN:34,PAGE_UP:33,PERIOD:190,RIGHT:39,SHIFT:16,SPACE:32,TAB:9,UP:38}};if(d){var f=c.attr,e=c.fn.removeAttr,h="http://www.w3.org/2005/07/aaa",a=/^aria-/,b=/^wairole:/;c.attr=function(k,j,l){var m=l!==undefined;return(j=="role"?(m?f.call(this,k,j,"wairole:"+l):(f.apply(this,arguments)||"").replace(b,"")):(a.test(j)?(m?k.setAttributeNS(h,j.replace(a,"aaa:"),l):f.call(this,k,j.replace(a,"aaa:"))):f.apply(this,arguments)))};c.fn.removeAttr=function(j){return(a.test(j)?this.each(function(){this.removeAttributeNS(h,j.replace(a,""))}):e.call(this,j))}}c.fn.extend({remove:function(){c("*",this).add(this).each(function(){c(this).triggerHandler("remove")});return i.apply(this,arguments)},enableSelection:function(){return this.attr("unselectable","off").css("MozUserSelect","").unbind("selectstart.ui")},disableSelection:function(){return this.attr("unselectable","on").css("MozUserSelect","none").bind("selectstart.ui",function(){return false})},scrollParent:function(){var j;if((c.browser.msie&&(/(static|relative)/).test(this.css("position")))||(/absolute/).test(this.css("position"))){j=this.parents().filter(function(){return(/(relative|absolute|fixed)/).test(c.curCSS(this,"position",1))&&(/(auto|scroll)/).test(c.curCSS(this,"overflow",1)+c.curCSS(this,"overflow-y",1)+c.curCSS(this,"overflow-x",1))}).eq(0)}else{j=this.parents().filter(function(){return(/(auto|scroll)/).test(c.curCSS(this,"overflow",1)+c.curCSS(this,"overflow-y",1)+c.curCSS(this,"overflow-x",1))}).eq(0)}return(/fixed/).test(this.css("position"))||!j.length?c(document):j}});c.extend(c.expr[":"],{data:function(l,k,j){return !!c.data(l,j[3])},focusable:function(k){var l=k.nodeName.toLowerCase(),j=c.attr(k,"tabindex");return(/input|select|textarea|button|object/.test(l)?!k.disabled:"a"==l||"area"==l?k.href||!isNaN(j):!isNaN(j))&&!c(k)["area"==l?"parents":"closest"](":hidden").length},tabbable:function(k){var j=c.attr(k,"tabindex");return(isNaN(j)||j>=0)&&c(k).is(":focusable")}});function g(m,n,o,l){function k(q){var p=c[m][n][q]||[];return(typeof p=="string"?p.split(/,?\s+/):p)}var j=k("getter");if(l.length==1&&typeof l[0]=="string"){j=j.concat(k("getterSetter"))}return(c.inArray(o,j)!=-1)}c.widget=function(k,j){var l=k.split(".")[0];k=k.split(".")[1];c.fn[k]=function(p){var n=(typeof p=="string"),o=Array.prototype.slice.call(arguments,1);if(n&&p.substring(0,1)=="_"){return this}if(n&&g(l,k,p,o)){var m=c.data(this[0],k);return(m?m[p].apply(m,o):undefined)}return this.each(function(){var q=c.data(this,k);(!q&&!n&&c.data(this,k,new c[l][k](this,p))._init());(q&&n&&c.isFunction(q[p])&&q[p].apply(q,o))})};c[l]=c[l]||{};c[l][k]=function(o,n){var m=this;this.namespace=l;this.widgetName=k;this.widgetEventPrefix=c[l][k].eventPrefix||k;this.widgetBaseClass=l+"-"+k;this.options=c.extend({},c.widget.defaults,c[l][k].defaults,c.metadata&&c.metadata.get(o)[k],n);this.element=c(o).bind("setData."+k,function(q,p,r){if(q.target==o){return m._setData(p,r)}}).bind("getData."+k,function(q,p){if(q.target==o){return m._getData(p)}}).bind("remove",function(){return m.destroy()})};c[l][k].prototype=c.extend({},c.widget.prototype,j);c[l][k].getterSetter="option"};c.widget.prototype={_init:function(){},destroy:function(){this.element.removeData(this.widgetName).removeClass(this.widgetBaseClass+"-disabled "+this.namespace+"-state-disabled").removeAttr("aria-disabled")},option:function(l,m){var k=l,j=this;if(typeof l=="string"){if(m===undefined){return this._getData(l)}k={};k[l]=m}c.each(k,function(n,o){j._setData(n,o)})},_getData:function(j){return this.options[j]},_setData:function(j,k){this.options[j]=k;if(j=="disabled"){this.element[k?"addClass":"removeClass"](this.widgetBaseClass+"-disabled "+this.namespace+"-state-disabled").attr("aria-disabled",k)}},enable:function(){this._setData("disabled",false)},disable:function(){this._setData("disabled",true)},_trigger:function(l,m,n){var p=this.options[l],j=(l==this.widgetEventPrefix?l:this.widgetEventPrefix+l);m=c.Event(m);m.type=j;if(m.originalEvent){for(var k=c.event.props.length,o;k;){o=c.event.props[--k];m[o]=m.originalEvent[o]}}this.element.trigger(m,n);return !(c.isFunction(p)&&p.call(this.element[0],m,n)===false||m.isDefaultPrevented())}};c.widget.defaults={disabled:false};c.ui.mouse={_mouseInit:function(){var j=this;this.element.bind("mousedown."+this.widgetName,function(k){return j._mouseDown(k)}).bind("click."+this.widgetName,function(k){if(j._preventClickEvent){j._preventClickEvent=false;k.stopImmediatePropagation();return false}});if(c.browser.msie){this._mouseUnselectable=this.element.attr("unselectable");this.element.attr("unselectable","on")}this.started=false},_mouseDestroy:function(){this.element.unbind("."+this.widgetName);(c.browser.msie&&this.element.attr("unselectable",this._mouseUnselectable))},_mouseDown:function(l){l.originalEvent=l.originalEvent||{};if(l.originalEvent.mouseHandled){return}(this._mouseStarted&&this._mouseUp(l));this._mouseDownEvent=l;var k=this,m=(l.which==1),j=(typeof this.options.cancel=="string"?c(l.target).parents().add(l.target).filter(this.options.cancel).length:false);if(!m||j||!this._mouseCapture(l)){return true}this.mouseDelayMet=!this.options.delay;if(!this.mouseDelayMet){this._mouseDelayTimer=setTimeout(function(){k.mouseDelayMet=true},this.options.delay)}if(this._mouseDistanceMet(l)&&this._mouseDelayMet(l)){this._mouseStarted=(this._mouseStart(l)!==false);if(!this._mouseStarted){l.preventDefault();return true}}this._mouseMoveDelegate=function(n){return k._mouseMove(n)};this._mouseUpDelegate=function(n){return k._mouseUp(n)};c(document).bind("mousemove."+this.widgetName,this._mouseMoveDelegate).bind("mouseup."+this.widgetName,this._mouseUpDelegate);(c.browser.safari||l.preventDefault());l.originalEvent.mouseHandled=true;return true},_mouseMove:function(j){if(c.browser.msie&&!j.button){return this._mouseUp(j)}if(this._mouseStarted){this._mouseDrag(j);return j.preventDefault()}if(this._mouseDistanceMet(j)&&this._mouseDelayMet(j)){this._mouseStarted=(this._mouseStart(this._mouseDownEvent,j)!==false);(this._mouseStarted?this._mouseDrag(j):this._mouseUp(j))}return !this._mouseStarted},_mouseUp:function(j){c(document).unbind("mousemove."+this.widgetName,this._mouseMoveDelegate).unbind("mouseup."+this.widgetName,this._mouseUpDelegate);if(this._mouseStarted){this._mouseStarted=false;this._preventClickEvent=(j.target==this._mouseDownEvent.target);this._mouseStop(j)}return false},_mouseDistanceMet:function(j){return(Math.max(Math.abs(this._mouseDownEvent.pageX-j.pageX),Math.abs(this._mouseDownEvent.pageY-j.pageY))>=this.options.distance)},_mouseDelayMet:function(j){return this.mouseDelayMet},_mouseStart:function(j){},_mouseDrag:function(j){},_mouseStop:function(j){},_mouseCapture:function(j){return true}};c.ui.mouse.defaults={cancel:null,distance:1,delay:0}})(jQuery);;
/*
 * jQuery UI Draggable 1.7.2
 *
 * Copyright (c) 2009 AUTHORS.txt (http://jqueryui.com/about)
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI/Draggables
 *
 * Depends:
 *	ui.core.js
 */
(function(a){a.widget("ui.draggable",a.extend({},a.ui.mouse,{_init:function(){if(this.options.helper=="original"&&!(/^(?:r|a|f)/).test(this.element.css("position"))){this.element[0].style.position="relative"}(this.options.addClasses&&this.element.addClass("ui-draggable"));(this.options.disabled&&this.element.addClass("ui-draggable-disabled"));this._mouseInit()},destroy:function(){if(!this.element.data("draggable")){return}this.element.removeData("draggable").unbind(".draggable").removeClass("ui-draggable ui-draggable-dragging ui-draggable-disabled");this._mouseDestroy()},_mouseCapture:function(b){var c=this.options;if(this.helper||c.disabled||a(b.target).is(".ui-resizable-handle")){return false}this.handle=this._getHandle(b);if(!this.handle){return false}return true},_mouseStart:function(b){var c=this.options;this.helper=this._createHelper(b);this._cacheHelperProportions();if(a.ui.ddmanager){a.ui.ddmanager.current=this}this._cacheMargins();this.cssPosition=this.helper.css("position");this.scrollParent=this.helper.scrollParent();this.offset=this.element.offset();this.offset={top:this.offset.top-this.margins.top,left:this.offset.left-this.margins.left};a.extend(this.offset,{click:{left:b.pageX-this.offset.left,top:b.pageY-this.offset.top},parent:this._getParentOffset(),relative:this._getRelativeOffset()});this.originalPosition=this._generatePosition(b);this.originalPageX=b.pageX;this.originalPageY=b.pageY;if(c.cursorAt){this._adjustOffsetFromHelper(c.cursorAt)}if(c.containment){this._setContainment()}this._trigger("start",b);this._cacheHelperProportions();if(a.ui.ddmanager&&!c.dropBehaviour){a.ui.ddmanager.prepareOffsets(this,b)}this.helper.addClass("ui-draggable-dragging");this._mouseDrag(b,true);return true},_mouseDrag:function(b,d){this.position=this._generatePosition(b);this.positionAbs=this._convertPositionTo("absolute");if(!d){var c=this._uiHash();this._trigger("drag",b,c);this.position=c.position}if(!this.options.axis||this.options.axis!="y"){this.helper[0].style.left=this.position.left+"px"}if(!this.options.axis||this.options.axis!="x"){this.helper[0].style.top=this.position.top+"px"}if(a.ui.ddmanager){a.ui.ddmanager.drag(this,b)}return false},_mouseStop:function(c){var d=false;if(a.ui.ddmanager&&!this.options.dropBehaviour){d=a.ui.ddmanager.drop(this,c)}if(this.dropped){d=this.dropped;this.dropped=false}if((this.options.revert=="invalid"&&!d)||(this.options.revert=="valid"&&d)||this.options.revert===true||(a.isFunction(this.options.revert)&&this.options.revert.call(this.element,d))){var b=this;a(this.helper).animate(this.originalPosition,parseInt(this.options.revertDuration,10),function(){b._trigger("stop",c);b._clear()})}else{this._trigger("stop",c);this._clear()}return false},_getHandle:function(b){var c=!this.options.handle||!a(this.options.handle,this.element).length?true:false;a(this.options.handle,this.element).find("*").andSelf().each(function(){if(this==b.target){c=true}});return c},_createHelper:function(c){var d=this.options;var b=a.isFunction(d.helper)?a(d.helper.apply(this.element[0],[c])):(d.helper=="clone"?this.element.clone():this.element);if(!b.parents("body").length){b.appendTo((d.appendTo=="parent"?this.element[0].parentNode:d.appendTo))}if(b[0]!=this.element[0]&&!(/(fixed|absolute)/).test(b.css("position"))){b.css("position","absolute")}return b},_adjustOffsetFromHelper:function(b){if(b.left!=undefined){this.offset.click.left=b.left+this.margins.left}if(b.right!=undefined){this.offset.click.left=this.helperProportions.width-b.right+this.margins.left}if(b.top!=undefined){this.offset.click.top=b.top+this.margins.top}if(b.bottom!=undefined){this.offset.click.top=this.helperProportions.height-b.bottom+this.margins.top}},_getParentOffset:function(){this.offsetParent=this.helper.offsetParent();var b=this.offsetParent.offset();if(this.cssPosition=="absolute"&&this.scrollParent[0]!=document&&a.ui.contains(this.scrollParent[0],this.offsetParent[0])){b.left+=this.scrollParent.scrollLeft();b.top+=this.scrollParent.scrollTop()}if((this.offsetParent[0]==document.body)||(this.offsetParent[0].tagName&&this.offsetParent[0].tagName.toLowerCase()=="html"&&a.browser.msie)){b={top:0,left:0}}return{top:b.top+(parseInt(this.offsetParent.css("borderTopWidth"),10)||0),left:b.left+(parseInt(this.offsetParent.css("borderLeftWidth"),10)||0)}},_getRelativeOffset:function(){if(this.cssPosition=="relative"){var b=this.element.position();return{top:b.top-(parseInt(this.helper.css("top"),10)||0)+this.scrollParent.scrollTop(),left:b.left-(parseInt(this.helper.css("left"),10)||0)+this.scrollParent.scrollLeft()}}else{return{top:0,left:0}}},_cacheMargins:function(){this.margins={left:(parseInt(this.element.css("marginLeft"),10)||0),top:(parseInt(this.element.css("marginTop"),10)||0)}},_cacheHelperProportions:function(){this.helperProportions={width:this.helper.outerWidth(),height:this.helper.outerHeight()}},_setContainment:function(){var e=this.options;if(e.containment=="parent"){e.containment=this.helper[0].parentNode}if(e.containment=="document"||e.containment=="window"){this.containment=[0-this.offset.relative.left-this.offset.parent.left,0-this.offset.relative.top-this.offset.parent.top,a(e.containment=="document"?document:window).width()-this.helperProportions.width-this.margins.left,(a(e.containment=="document"?document:window).height()||document.body.parentNode.scrollHeight)-this.helperProportions.height-this.margins.top]}if(!(/^(document|window|parent)$/).test(e.containment)&&e.containment.constructor!=Array){var c=a(e.containment)[0];if(!c){return}var d=a(e.containment).offset();var b=(a(c).css("overflow")!="hidden");this.containment=[d.left+(parseInt(a(c).css("borderLeftWidth"),10)||0)+(parseInt(a(c).css("paddingLeft"),10)||0)-this.margins.left,d.top+(parseInt(a(c).css("borderTopWidth"),10)||0)+(parseInt(a(c).css("paddingTop"),10)||0)-this.margins.top,d.left+(b?Math.max(c.scrollWidth,c.offsetWidth):c.offsetWidth)-(parseInt(a(c).css("borderLeftWidth"),10)||0)-(parseInt(a(c).css("paddingRight"),10)||0)-this.helperProportions.width-this.margins.left,d.top+(b?Math.max(c.scrollHeight,c.offsetHeight):c.offsetHeight)-(parseInt(a(c).css("borderTopWidth"),10)||0)-(parseInt(a(c).css("paddingBottom"),10)||0)-this.helperProportions.height-this.margins.top]}else{if(e.containment.constructor==Array){this.containment=e.containment}}},_convertPositionTo:function(f,h){if(!h){h=this.position}var c=f=="absolute"?1:-1;var e=this.options,b=this.cssPosition=="absolute"&&!(this.scrollParent[0]!=document&&a.ui.contains(this.scrollParent[0],this.offsetParent[0]))?this.offsetParent:this.scrollParent,g=(/(html|body)/i).test(b[0].tagName);return{top:(h.top+this.offset.relative.top*c+this.offset.parent.top*c-(a.browser.safari&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollTop():(g?0:b.scrollTop()))*c)),left:(h.left+this.offset.relative.left*c+this.offset.parent.left*c-(a.browser.safari&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollLeft():g?0:b.scrollLeft())*c))}},_generatePosition:function(e){var h=this.options,b=this.cssPosition=="absolute"&&!(this.scrollParent[0]!=document&&a.ui.contains(this.scrollParent[0],this.offsetParent[0]))?this.offsetParent:this.scrollParent,i=(/(html|body)/i).test(b[0].tagName);if(this.cssPosition=="relative"&&!(this.scrollParent[0]!=document&&this.scrollParent[0]!=this.offsetParent[0])){this.offset.relative=this._getRelativeOffset()}var d=e.pageX;var c=e.pageY;if(this.originalPosition){if(this.containment){if(e.pageX-this.offset.click.left<this.containment[0]){d=this.containment[0]+this.offset.click.left}if(e.pageY-this.offset.click.top<this.containment[1]){c=this.containment[1]+this.offset.click.top}if(e.pageX-this.offset.click.left>this.containment[2]){d=this.containment[2]+this.offset.click.left}if(e.pageY-this.offset.click.top>this.containment[3]){c=this.containment[3]+this.offset.click.top}}if(h.grid){var g=this.originalPageY+Math.round((c-this.originalPageY)/h.grid[1])*h.grid[1];c=this.containment?(!(g-this.offset.click.top<this.containment[1]||g-this.offset.click.top>this.containment[3])?g:(!(g-this.offset.click.top<this.containment[1])?g-h.grid[1]:g+h.grid[1])):g;var f=this.originalPageX+Math.round((d-this.originalPageX)/h.grid[0])*h.grid[0];d=this.containment?(!(f-this.offset.click.left<this.containment[0]||f-this.offset.click.left>this.containment[2])?f:(!(f-this.offset.click.left<this.containment[0])?f-h.grid[0]:f+h.grid[0])):f}}return{top:(c-this.offset.click.top-this.offset.relative.top-this.offset.parent.top+(a.browser.safari&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollTop():(i?0:b.scrollTop())))),left:(d-this.offset.click.left-this.offset.relative.left-this.offset.parent.left+(a.browser.safari&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollLeft():i?0:b.scrollLeft())))}},_clear:function(){this.helper.removeClass("ui-draggable-dragging");if(this.helper[0]!=this.element[0]&&!this.cancelHelperRemoval){this.helper.remove()}this.helper=null;this.cancelHelperRemoval=false},_trigger:function(b,c,d){d=d||this._uiHash();a.ui.plugin.call(this,b,[c,d]);if(b=="drag"){this.positionAbs=this._convertPositionTo("absolute")}return a.widget.prototype._trigger.call(this,b,c,d)},plugins:{},_uiHash:function(b){return{helper:this.helper,position:this.position,absolutePosition:this.positionAbs,offset:this.positionAbs}}}));a.extend(a.ui.draggable,{version:"1.7.2",eventPrefix:"drag",defaults:{addClasses:true,appendTo:"parent",axis:false,cancel:":input,option",connectToSortable:false,containment:false,cursor:"auto",cursorAt:false,delay:0,distance:1,grid:false,handle:false,helper:"original",iframeFix:false,opacity:false,refreshPositions:false,revert:false,revertDuration:500,scope:"default",scroll:true,scrollSensitivity:20,scrollSpeed:20,snap:false,snapMode:"both",snapTolerance:20,stack:false,zIndex:false}});a.ui.plugin.add("draggable","connectToSortable",{start:function(c,e){var d=a(this).data("draggable"),f=d.options,b=a.extend({},e,{item:d.element});d.sortables=[];a(f.connectToSortable).each(function(){var g=a.data(this,"sortable");if(g&&!g.options.disabled){d.sortables.push({instance:g,shouldRevert:g.options.revert});g._refreshItems();g._trigger("activate",c,b)}})},stop:function(c,e){var d=a(this).data("draggable"),b=a.extend({},e,{item:d.element});a.each(d.sortables,function(){if(this.instance.isOver){this.instance.isOver=0;d.cancelHelperRemoval=true;this.instance.cancelHelperRemoval=false;if(this.shouldRevert){this.instance.options.revert=true}this.instance._mouseStop(c);this.instance.options.helper=this.instance.options._helper;if(d.options.helper=="original"){this.instance.currentItem.css({top:"auto",left:"auto"})}}else{this.instance.cancelHelperRemoval=false;this.instance._trigger("deactivate",c,b)}})},drag:function(c,f){var e=a(this).data("draggable"),b=this;var d=function(i){var n=this.offset.click.top,m=this.offset.click.left;var g=this.positionAbs.top,k=this.positionAbs.left;var j=i.height,l=i.width;var p=i.top,h=i.left;return a.ui.isOver(g+n,k+m,p,h,j,l)};a.each(e.sortables,function(g){this.instance.positionAbs=e.positionAbs;this.instance.helperProportions=e.helperProportions;this.instance.offset.click=e.offset.click;if(this.instance._intersectsWith(this.instance.containerCache)){if(!this.instance.isOver){this.instance.isOver=1;this.instance.currentItem=a(b).clone().appendTo(this.instance.element).data("sortable-item",true);this.instance.options._helper=this.instance.options.helper;this.instance.options.helper=function(){return f.helper[0]};c.target=this.instance.currentItem[0];this.instance._mouseCapture(c,true);this.instance._mouseStart(c,true,true);this.instance.offset.click.top=e.offset.click.top;this.instance.offset.click.left=e.offset.click.left;this.instance.offset.parent.left-=e.offset.parent.left-this.instance.offset.parent.left;this.instance.offset.parent.top-=e.offset.parent.top-this.instance.offset.parent.top;e._trigger("toSortable",c);e.dropped=this.instance.element;e.currentItem=e.element;this.instance.fromOutside=e}if(this.instance.currentItem){this.instance._mouseDrag(c)}}else{if(this.instance.isOver){this.instance.isOver=0;this.instance.cancelHelperRemoval=true;this.instance.options.revert=false;this.instance._trigger("out",c,this.instance._uiHash(this.instance));this.instance._mouseStop(c,true);this.instance.options.helper=this.instance.options._helper;this.instance.currentItem.remove();if(this.instance.placeholder){this.instance.placeholder.remove()}e._trigger("fromSortable",c);e.dropped=false}}})}});a.ui.plugin.add("draggable","cursor",{start:function(c,d){var b=a("body"),e=a(this).data("draggable").options;if(b.css("cursor")){e._cursor=b.css("cursor")}b.css("cursor",e.cursor)},stop:function(b,c){var d=a(this).data("draggable").options;if(d._cursor){a("body").css("cursor",d._cursor)}}});a.ui.plugin.add("draggable","iframeFix",{start:function(b,c){var d=a(this).data("draggable").options;a(d.iframeFix===true?"iframe":d.iframeFix).each(function(){a('<div class="ui-draggable-iframeFix" style="background: #fff;"></div>').css({width:this.offsetWidth+"px",height:this.offsetHeight+"px",position:"absolute",opacity:"0.001",zIndex:1000}).css(a(this).offset()).appendTo("body")})},stop:function(b,c){a("div.ui-draggable-iframeFix").each(function(){this.parentNode.removeChild(this)})}});a.ui.plugin.add("draggable","opacity",{start:function(c,d){var b=a(d.helper),e=a(this).data("draggable").options;if(b.css("opacity")){e._opacity=b.css("opacity")}b.css("opacity",e.opacity)},stop:function(b,c){var d=a(this).data("draggable").options;if(d._opacity){a(c.helper).css("opacity",d._opacity)}}});a.ui.plugin.add("draggable","scroll",{start:function(c,d){var b=a(this).data("draggable");if(b.scrollParent[0]!=document&&b.scrollParent[0].tagName!="HTML"){b.overflowOffset=b.scrollParent.offset()}},drag:function(d,e){var c=a(this).data("draggable"),f=c.options,b=false;if(c.scrollParent[0]!=document&&c.scrollParent[0].tagName!="HTML"){if(!f.axis||f.axis!="x"){if((c.overflowOffset.top+c.scrollParent[0].offsetHeight)-d.pageY<f.scrollSensitivity){c.scrollParent[0].scrollTop=b=c.scrollParent[0].scrollTop+f.scrollSpeed}else{if(d.pageY-c.overflowOffset.top<f.scrollSensitivity){c.scrollParent[0].scrollTop=b=c.scrollParent[0].scrollTop-f.scrollSpeed}}}if(!f.axis||f.axis!="y"){if((c.overflowOffset.left+c.scrollParent[0].offsetWidth)-d.pageX<f.scrollSensitivity){c.scrollParent[0].scrollLeft=b=c.scrollParent[0].scrollLeft+f.scrollSpeed}else{if(d.pageX-c.overflowOffset.left<f.scrollSensitivity){c.scrollParent[0].scrollLeft=b=c.scrollParent[0].scrollLeft-f.scrollSpeed}}}}else{if(!f.axis||f.axis!="x"){if(d.pageY-a(document).scrollTop()<f.scrollSensitivity){b=a(document).scrollTop(a(document).scrollTop()-f.scrollSpeed)}else{if(a(window).height()-(d.pageY-a(document).scrollTop())<f.scrollSensitivity){b=a(document).scrollTop(a(document).scrollTop()+f.scrollSpeed)}}}if(!f.axis||f.axis!="y"){if(d.pageX-a(document).scrollLeft()<f.scrollSensitivity){b=a(document).scrollLeft(a(document).scrollLeft()-f.scrollSpeed)}else{if(a(window).width()-(d.pageX-a(document).scrollLeft())<f.scrollSensitivity){b=a(document).scrollLeft(a(document).scrollLeft()+f.scrollSpeed)}}}}if(b!==false&&a.ui.ddmanager&&!f.dropBehaviour){a.ui.ddmanager.prepareOffsets(c,d)}}});a.ui.plugin.add("draggable","snap",{start:function(c,d){var b=a(this).data("draggable"),e=b.options;b.snapElements=[];a(e.snap.constructor!=String?(e.snap.items||":data(draggable)"):e.snap).each(function(){var g=a(this);var f=g.offset();if(this!=b.element[0]){b.snapElements.push({item:this,width:g.outerWidth(),height:g.outerHeight(),top:f.top,left:f.left})}})},drag:function(u,p){var g=a(this).data("draggable"),q=g.options;var y=q.snapTolerance;var x=p.offset.left,w=x+g.helperProportions.width,f=p.offset.top,e=f+g.helperProportions.height;for(var v=g.snapElements.length-1;v>=0;v--){var s=g.snapElements[v].left,n=s+g.snapElements[v].width,m=g.snapElements[v].top,A=m+g.snapElements[v].height;if(!((s-y<x&&x<n+y&&m-y<f&&f<A+y)||(s-y<x&&x<n+y&&m-y<e&&e<A+y)||(s-y<w&&w<n+y&&m-y<f&&f<A+y)||(s-y<w&&w<n+y&&m-y<e&&e<A+y))){if(g.snapElements[v].snapping){(g.options.snap.release&&g.options.snap.release.call(g.element,u,a.extend(g._uiHash(),{snapItem:g.snapElements[v].item})))}g.snapElements[v].snapping=false;continue}if(q.snapMode!="inner"){var c=Math.abs(m-e)<=y;var z=Math.abs(A-f)<=y;var j=Math.abs(s-w)<=y;var k=Math.abs(n-x)<=y;if(c){p.position.top=g._convertPositionTo("relative",{top:m-g.helperProportions.height,left:0}).top-g.margins.top}if(z){p.position.top=g._convertPositionTo("relative",{top:A,left:0}).top-g.margins.top}if(j){p.position.left=g._convertPositionTo("relative",{top:0,left:s-g.helperProportions.width}).left-g.margins.left}if(k){p.position.left=g._convertPositionTo("relative",{top:0,left:n}).left-g.margins.left}}var h=(c||z||j||k);if(q.snapMode!="outer"){var c=Math.abs(m-f)<=y;var z=Math.abs(A-e)<=y;var j=Math.abs(s-x)<=y;var k=Math.abs(n-w)<=y;if(c){p.position.top=g._convertPositionTo("relative",{top:m,left:0}).top-g.margins.top}if(z){p.position.top=g._convertPositionTo("relative",{top:A-g.helperProportions.height,left:0}).top-g.margins.top}if(j){p.position.left=g._convertPositionTo("relative",{top:0,left:s}).left-g.margins.left}if(k){p.position.left=g._convertPositionTo("relative",{top:0,left:n-g.helperProportions.width}).left-g.margins.left}}if(!g.snapElements[v].snapping&&(c||z||j||k||h)){(g.options.snap.snap&&g.options.snap.snap.call(g.element,u,a.extend(g._uiHash(),{snapItem:g.snapElements[v].item})))}g.snapElements[v].snapping=(c||z||j||k||h)}}});a.ui.plugin.add("draggable","stack",{start:function(b,c){var e=a(this).data("draggable").options;var d=a.makeArray(a(e.stack.group)).sort(function(g,f){return(parseInt(a(g).css("zIndex"),10)||e.stack.min)-(parseInt(a(f).css("zIndex"),10)||e.stack.min)});a(d).each(function(f){this.style.zIndex=e.stack.min+f});this[0].style.zIndex=e.stack.min+d.length}});a.ui.plugin.add("draggable","zIndex",{start:function(c,d){var b=a(d.helper),e=a(this).data("draggable").options;if(b.css("zIndex")){e._zIndex=b.css("zIndex")}b.css("zIndex",e.zIndex)},stop:function(b,c){var d=a(this).data("draggable").options;if(d._zIndex){a(c.helper).css("zIndex",d._zIndex)}}})})(jQuery);;
/*
 * jQuery UI Resizable 1.7.2
 *
 * Copyright (c) 2009 AUTHORS.txt (http://jqueryui.com/about)
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI/Resizables
 *
 * Depends:
 *	ui.core.js
 */
(function(c){c.widget("ui.resizable",c.extend({},c.ui.mouse,{_init:function(){var e=this,j=this.options;this.element.addClass("ui-resizable");c.extend(this,{_aspectRatio:!!(j.aspectRatio),aspectRatio:j.aspectRatio,originalElement:this.element,_proportionallyResizeElements:[],_helper:j.helper||j.ghost||j.animate?j.helper||"ui-resizable-helper":null});if(this.element[0].nodeName.match(/canvas|textarea|input|select|button|img/i)){if(/relative/.test(this.element.css("position"))&&c.browser.opera){this.element.css({position:"relative",top:"auto",left:"auto"})}this.element.wrap(c('<div class="ui-wrapper" style="overflow: hidden;"></div>').css({position:this.element.css("position"),width:this.element.outerWidth(),height:this.element.outerHeight(),top:this.element.css("top"),left:this.element.css("left")}));this.element=this.element.parent().data("resizable",this.element.data("resizable"));this.elementIsWrapper=true;this.element.css({marginLeft:this.originalElement.css("marginLeft"),marginTop:this.originalElement.css("marginTop"),marginRight:this.originalElement.css("marginRight"),marginBottom:this.originalElement.css("marginBottom")});this.originalElement.css({marginLeft:0,marginTop:0,marginRight:0,marginBottom:0});this.originalResizeStyle=this.originalElement.css("resize");this.originalElement.css("resize","none");this._proportionallyResizeElements.push(this.originalElement.css({position:"static",zoom:1,display:"block"}));this.originalElement.css({margin:this.originalElement.css("margin")});this._proportionallyResize()}this.handles=j.handles||(!c(".ui-resizable-handle",this.element).length?"e,s,se":{n:".ui-resizable-n",e:".ui-resizable-e",s:".ui-resizable-s",w:".ui-resizable-w",se:".ui-resizable-se",sw:".ui-resizable-sw",ne:".ui-resizable-ne",nw:".ui-resizable-nw"});if(this.handles.constructor==String){if(this.handles=="all"){this.handles="n,e,s,w,se,sw,ne,nw"}var k=this.handles.split(",");this.handles={};for(var f=0;f<k.length;f++){var h=c.trim(k[f]),d="ui-resizable-"+h;var g=c('<div class="ui-resizable-handle '+d+'"></div>');if(/sw|se|ne|nw/.test(h)){g.css({zIndex:++j.zIndex})}if("se"==h){g.addClass("ui-icon ui-icon-gripsmall-diagonal-se")}this.handles[h]=".ui-resizable-"+h;this.element.append(g)}}this._renderAxis=function(p){p=p||this.element;for(var m in this.handles){if(this.handles[m].constructor==String){this.handles[m]=c(this.handles[m],this.element).show()}if(this.elementIsWrapper&&this.originalElement[0].nodeName.match(/textarea|input|select|button/i)){var n=c(this.handles[m],this.element),o=0;o=/sw|ne|nw|se|n|s/.test(m)?n.outerHeight():n.outerWidth();var l=["padding",/ne|nw|n/.test(m)?"Top":/se|sw|s/.test(m)?"Bottom":/^e$/.test(m)?"Right":"Left"].join("");p.css(l,o);this._proportionallyResize()}if(!c(this.handles[m]).length){continue}}};this._renderAxis(this.element);this._handles=c(".ui-resizable-handle",this.element).disableSelection();this._handles.mouseover(function(){if(!e.resizing){if(this.className){var i=this.className.match(/ui-resizable-(se|sw|ne|nw|n|e|s|w)/i)}e.axis=i&&i[1]?i[1]:"se"}});if(j.autoHide){this._handles.hide();c(this.element).addClass("ui-resizable-autohide").hover(function(){c(this).removeClass("ui-resizable-autohide");e._handles.show()},function(){if(!e.resizing){c(this).addClass("ui-resizable-autohide");e._handles.hide()}})}this._mouseInit()},destroy:function(){this._mouseDestroy();var d=function(f){c(f).removeClass("ui-resizable ui-resizable-disabled ui-resizable-resizing").removeData("resizable").unbind(".resizable").find(".ui-resizable-handle").remove()};if(this.elementIsWrapper){d(this.element);var e=this.element;e.parent().append(this.originalElement.css({position:e.css("position"),width:e.outerWidth(),height:e.outerHeight(),top:e.css("top"),left:e.css("left")})).end().remove()}this.originalElement.css("resize",this.originalResizeStyle);d(this.originalElement)},_mouseCapture:function(e){var f=false;for(var d in this.handles){if(c(this.handles[d])[0]==e.target){f=true}}return this.options.disabled||!!f},_mouseStart:function(f){var i=this.options,e=this.element.position(),d=this.element;this.resizing=true;this.documentScroll={top:c(document).scrollTop(),left:c(document).scrollLeft()};if(d.is(".ui-draggable")||(/absolute/).test(d.css("position"))){d.css({position:"absolute",top:e.top,left:e.left})}if(c.browser.opera&&(/relative/).test(d.css("position"))){d.css({position:"relative",top:"auto",left:"auto"})}this._renderProxy();var j=b(this.helper.css("left")),g=b(this.helper.css("top"));if(i.containment){j+=c(i.containment).scrollLeft()||0;g+=c(i.containment).scrollTop()||0}this.offset=this.helper.offset();this.position={left:j,top:g};this.size=this._helper?{width:d.outerWidth(),height:d.outerHeight()}:{width:d.width(),height:d.height()};this.originalSize=this._helper?{width:d.outerWidth(),height:d.outerHeight()}:{width:d.width(),height:d.height()};this.originalPosition={left:j,top:g};this.sizeDiff={width:d.outerWidth()-d.width(),height:d.outerHeight()-d.height()};this.originalMousePosition={left:f.pageX,top:f.pageY};this.aspectRatio=(typeof i.aspectRatio=="number")?i.aspectRatio:((this.originalSize.width/this.originalSize.height)||1);var h=c(".ui-resizable-"+this.axis).css("cursor");c("body").css("cursor",h=="auto"?this.axis+"-resize":h);d.addClass("ui-resizable-resizing");this._propagate("start",f);return true},_mouseDrag:function(d){var g=this.helper,f=this.options,l={},p=this,i=this.originalMousePosition,m=this.axis;var q=(d.pageX-i.left)||0,n=(d.pageY-i.top)||0;var h=this._change[m];if(!h){return false}var k=h.apply(this,[d,q,n]),j=c.browser.msie&&c.browser.version<7,e=this.sizeDiff;if(this._aspectRatio||d.shiftKey){k=this._updateRatio(k,d)}k=this._respectSize(k,d);this._propagate("resize",d);g.css({top:this.position.top+"px",left:this.position.left+"px",width:this.size.width+"px",height:this.size.height+"px"});if(!this._helper&&this._proportionallyResizeElements.length){this._proportionallyResize()}this._updateCache(k);this._trigger("resize",d,this.ui());return false},_mouseStop:function(g){this.resizing=false;var h=this.options,l=this;if(this._helper){var f=this._proportionallyResizeElements,d=f.length&&(/textarea/i).test(f[0].nodeName),e=d&&c.ui.hasScroll(f[0],"left")?0:l.sizeDiff.height,j=d?0:l.sizeDiff.width;var m={width:(l.size.width-j),height:(l.size.height-e)},i=(parseInt(l.element.css("left"),10)+(l.position.left-l.originalPosition.left))||null,k=(parseInt(l.element.css("top"),10)+(l.position.top-l.originalPosition.top))||null;if(!h.animate){this.element.css(c.extend(m,{top:k,left:i}))}l.helper.height(l.size.height);l.helper.width(l.size.width);if(this._helper&&!h.animate){this._proportionallyResize()}}c("body").css("cursor","auto");this.element.removeClass("ui-resizable-resizing");this._propagate("stop",g);if(this._helper){this.helper.remove()}return false},_updateCache:function(d){var e=this.options;this.offset=this.helper.offset();if(a(d.left)){this.position.left=d.left}if(a(d.top)){this.position.top=d.top}if(a(d.height)){this.size.height=d.height}if(a(d.width)){this.size.width=d.width}},_updateRatio:function(g,f){var h=this.options,i=this.position,e=this.size,d=this.axis;if(g.height){g.width=(e.height*this.aspectRatio)}else{if(g.width){g.height=(e.width/this.aspectRatio)}}if(d=="sw"){g.left=i.left+(e.width-g.width);g.top=null}if(d=="nw"){g.top=i.top+(e.height-g.height);g.left=i.left+(e.width-g.width)}return g},_respectSize:function(k,f){var i=this.helper,h=this.options,q=this._aspectRatio||f.shiftKey,p=this.axis,s=a(k.width)&&h.maxWidth&&(h.maxWidth<k.width),l=a(k.height)&&h.maxHeight&&(h.maxHeight<k.height),g=a(k.width)&&h.minWidth&&(h.minWidth>k.width),r=a(k.height)&&h.minHeight&&(h.minHeight>k.height);if(g){k.width=h.minWidth}if(r){k.height=h.minHeight}if(s){k.width=h.maxWidth}if(l){k.height=h.maxHeight}var e=this.originalPosition.left+this.originalSize.width,n=this.position.top+this.size.height;var j=/sw|nw|w/.test(p),d=/nw|ne|n/.test(p);if(g&&j){k.left=e-h.minWidth}if(s&&j){k.left=e-h.maxWidth}if(r&&d){k.top=n-h.minHeight}if(l&&d){k.top=n-h.maxHeight}var m=!k.width&&!k.height;if(m&&!k.left&&k.top){k.top=null}else{if(m&&!k.top&&k.left){k.left=null}}return k},_proportionallyResize:function(){var j=this.options;if(!this._proportionallyResizeElements.length){return}var f=this.helper||this.element;for(var e=0;e<this._proportionallyResizeElements.length;e++){var g=this._proportionallyResizeElements[e];if(!this.borderDif){var d=[g.css("borderTopWidth"),g.css("borderRightWidth"),g.css("borderBottomWidth"),g.css("borderLeftWidth")],h=[g.css("paddingTop"),g.css("paddingRight"),g.css("paddingBottom"),g.css("paddingLeft")];this.borderDif=c.map(d,function(k,m){var l=parseInt(k,10)||0,n=parseInt(h[m],10)||0;return l+n})}if(c.browser.msie&&!(!(c(f).is(":hidden")||c(f).parents(":hidden").length))){continue}g.css({height:(f.height()-this.borderDif[0]-this.borderDif[2])||0,width:(f.width()-this.borderDif[1]-this.borderDif[3])||0})}},_renderProxy:function(){var e=this.element,h=this.options;this.elementOffset=e.offset();if(this._helper){this.helper=this.helper||c('<div style="overflow:hidden;"></div>');var d=c.browser.msie&&c.browser.version<7,f=(d?1:0),g=(d?2:-1);this.helper.addClass(this._helper).css({width:this.element.outerWidth()+g,height:this.element.outerHeight()+g,position:"absolute",left:this.elementOffset.left-f+"px",top:this.elementOffset.top-f+"px",zIndex:++h.zIndex});this.helper.appendTo("body").disableSelection()}else{this.helper=this.element}},_change:{e:function(f,e,d){return{width:this.originalSize.width+e}},w:function(g,e,d){var i=this.options,f=this.originalSize,h=this.originalPosition;return{left:h.left+e,width:f.width-e}},n:function(g,e,d){var i=this.options,f=this.originalSize,h=this.originalPosition;return{top:h.top+d,height:f.height-d}},s:function(f,e,d){return{height:this.originalSize.height+d}},se:function(f,e,d){return c.extend(this._change.s.apply(this,arguments),this._change.e.apply(this,[f,e,d]))},sw:function(f,e,d){return c.extend(this._change.s.apply(this,arguments),this._change.w.apply(this,[f,e,d]))},ne:function(f,e,d){return c.extend(this._change.n.apply(this,arguments),this._change.e.apply(this,[f,e,d]))},nw:function(f,e,d){return c.extend(this._change.n.apply(this,arguments),this._change.w.apply(this,[f,e,d]))}},_propagate:function(e,d){c.ui.plugin.call(this,e,[d,this.ui()]);(e!="resize"&&this._trigger(e,d,this.ui()))},plugins:{},ui:function(){return{originalElement:this.originalElement,element:this.element,helper:this.helper,position:this.position,size:this.size,originalSize:this.originalSize,originalPosition:this.originalPosition}}}));c.extend(c.ui.resizable,{version:"1.7.2",eventPrefix:"resize",defaults:{alsoResize:false,animate:false,animateDuration:"slow",animateEasing:"swing",aspectRatio:false,autoHide:false,cancel:":input,option",containment:false,delay:0,distance:1,ghost:false,grid:false,handles:"e,s,se",helper:false,maxHeight:null,maxWidth:null,minHeight:10,minWidth:10,zIndex:1000}});c.ui.plugin.add("resizable","alsoResize",{start:function(e,f){var d=c(this).data("resizable"),g=d.options;_store=function(h){c(h).each(function(){c(this).data("resizable-alsoresize",{width:parseInt(c(this).width(),10),height:parseInt(c(this).height(),10),left:parseInt(c(this).css("left"),10),top:parseInt(c(this).css("top"),10)})})};if(typeof(g.alsoResize)=="object"&&!g.alsoResize.parentNode){if(g.alsoResize.length){g.alsoResize=g.alsoResize[0];_store(g.alsoResize)}else{c.each(g.alsoResize,function(h,i){_store(h)})}}else{_store(g.alsoResize)}},resize:function(f,h){var e=c(this).data("resizable"),i=e.options,g=e.originalSize,k=e.originalPosition;var j={height:(e.size.height-g.height)||0,width:(e.size.width-g.width)||0,top:(e.position.top-k.top)||0,left:(e.position.left-k.left)||0},d=function(l,m){c(l).each(function(){var p=c(this),q=c(this).data("resizable-alsoresize"),o={},n=m&&m.length?m:["width","height","top","left"];c.each(n||["width","height","top","left"],function(r,t){var s=(q[t]||0)+(j[t]||0);if(s&&s>=0){o[t]=s||null}});if(/relative/.test(p.css("position"))&&c.browser.opera){e._revertToRelativePosition=true;p.css({position:"absolute",top:"auto",left:"auto"})}p.css(o)})};if(typeof(i.alsoResize)=="object"&&!i.alsoResize.nodeType){c.each(i.alsoResize,function(l,m){d(l,m)})}else{d(i.alsoResize)}},stop:function(e,f){var d=c(this).data("resizable");if(d._revertToRelativePosition&&c.browser.opera){d._revertToRelativePosition=false;el.css({position:"relative"})}c(this).removeData("resizable-alsoresize-start")}});c.ui.plugin.add("resizable","animate",{stop:function(h,m){var n=c(this).data("resizable"),i=n.options;var g=n._proportionallyResizeElements,d=g.length&&(/textarea/i).test(g[0].nodeName),e=d&&c.ui.hasScroll(g[0],"left")?0:n.sizeDiff.height,k=d?0:n.sizeDiff.width;var f={width:(n.size.width-k),height:(n.size.height-e)},j=(parseInt(n.element.css("left"),10)+(n.position.left-n.originalPosition.left))||null,l=(parseInt(n.element.css("top"),10)+(n.position.top-n.originalPosition.top))||null;n.element.animate(c.extend(f,l&&j?{top:l,left:j}:{}),{duration:i.animateDuration,easing:i.animateEasing,step:function(){var o={width:parseInt(n.element.css("width"),10),height:parseInt(n.element.css("height"),10),top:parseInt(n.element.css("top"),10),left:parseInt(n.element.css("left"),10)};if(g&&g.length){c(g[0]).css({width:o.width,height:o.height})}n._updateCache(o);n._propagate("resize",h)}})}});c.ui.plugin.add("resizable","containment",{start:function(e,q){var s=c(this).data("resizable"),i=s.options,k=s.element;var f=i.containment,j=(f instanceof c)?f.get(0):(/parent/.test(f))?k.parent().get(0):f;if(!j){return}s.containerElement=c(j);if(/document/.test(f)||f==document){s.containerOffset={left:0,top:0};s.containerPosition={left:0,top:0};s.parentData={element:c(document),left:0,top:0,width:c(document).width(),height:c(document).height()||document.body.parentNode.scrollHeight}}else{var m=c(j),h=[];c(["Top","Right","Left","Bottom"]).each(function(p,o){h[p]=b(m.css("padding"+o))});s.containerOffset=m.offset();s.containerPosition=m.position();s.containerSize={height:(m.innerHeight()-h[3]),width:(m.innerWidth()-h[1])};var n=s.containerOffset,d=s.containerSize.height,l=s.containerSize.width,g=(c.ui.hasScroll(j,"left")?j.scrollWidth:l),r=(c.ui.hasScroll(j)?j.scrollHeight:d);s.parentData={element:j,left:n.left,top:n.top,width:g,height:r}}},resize:function(f,p){var s=c(this).data("resizable"),h=s.options,e=s.containerSize,n=s.containerOffset,l=s.size,m=s.position,q=s._aspectRatio||f.shiftKey,d={top:0,left:0},g=s.containerElement;if(g[0]!=document&&(/static/).test(g.css("position"))){d=n}if(m.left<(s._helper?n.left:0)){s.size.width=s.size.width+(s._helper?(s.position.left-n.left):(s.position.left-d.left));if(q){s.size.height=s.size.width/h.aspectRatio}s.position.left=h.helper?n.left:0}if(m.top<(s._helper?n.top:0)){s.size.height=s.size.height+(s._helper?(s.position.top-n.top):s.position.top);if(q){s.size.width=s.size.height*h.aspectRatio}s.position.top=s._helper?n.top:0}s.offset.left=s.parentData.left+s.position.left;s.offset.top=s.parentData.top+s.position.top;var k=Math.abs((s._helper?s.offset.left-d.left:(s.offset.left-d.left))+s.sizeDiff.width),r=Math.abs((s._helper?s.offset.top-d.top:(s.offset.top-n.top))+s.sizeDiff.height);var j=s.containerElement.get(0)==s.element.parent().get(0),i=/relative|absolute/.test(s.containerElement.css("position"));if(j&&i){k-=s.parentData.left}if(k+s.size.width>=s.parentData.width){s.size.width=s.parentData.width-k;if(q){s.size.height=s.size.width/s.aspectRatio}}if(r+s.size.height>=s.parentData.height){s.size.height=s.parentData.height-r;if(q){s.size.width=s.size.height*s.aspectRatio}}},stop:function(e,m){var p=c(this).data("resizable"),f=p.options,k=p.position,l=p.containerOffset,d=p.containerPosition,g=p.containerElement;var i=c(p.helper),q=i.offset(),n=i.outerWidth()-p.sizeDiff.width,j=i.outerHeight()-p.sizeDiff.height;if(p._helper&&!f.animate&&(/relative/).test(g.css("position"))){c(this).css({left:q.left-d.left-l.left,width:n,height:j})}if(p._helper&&!f.animate&&(/static/).test(g.css("position"))){c(this).css({left:q.left-d.left-l.left,width:n,height:j})}}});c.ui.plugin.add("resizable","ghost",{start:function(f,g){var d=c(this).data("resizable"),h=d.options,e=d.size;d.ghost=d.originalElement.clone();d.ghost.css({opacity:0.25,display:"block",position:"relative",height:e.height,width:e.width,margin:0,left:0,top:0}).addClass("ui-resizable-ghost").addClass(typeof h.ghost=="string"?h.ghost:"");d.ghost.appendTo(d.helper)},resize:function(e,f){var d=c(this).data("resizable"),g=d.options;if(d.ghost){d.ghost.css({position:"relative",height:d.size.height,width:d.size.width})}},stop:function(e,f){var d=c(this).data("resizable"),g=d.options;if(d.ghost&&d.helper){d.helper.get(0).removeChild(d.ghost.get(0))}}});c.ui.plugin.add("resizable","grid",{resize:function(d,l){var n=c(this).data("resizable"),g=n.options,j=n.size,h=n.originalSize,i=n.originalPosition,m=n.axis,k=g._aspectRatio||d.shiftKey;g.grid=typeof g.grid=="number"?[g.grid,g.grid]:g.grid;var f=Math.round((j.width-h.width)/(g.grid[0]||1))*(g.grid[0]||1),e=Math.round((j.height-h.height)/(g.grid[1]||1))*(g.grid[1]||1);if(/^(se|s|e)$/.test(m)){n.size.width=h.width+f;n.size.height=h.height+e}else{if(/^(ne)$/.test(m)){n.size.width=h.width+f;n.size.height=h.height+e;n.position.top=i.top-e}else{if(/^(sw)$/.test(m)){n.size.width=h.width+f;n.size.height=h.height+e;n.position.left=i.left-f}else{n.size.width=h.width+f;n.size.height=h.height+e;n.position.top=i.top-e;n.position.left=i.left-f}}}}});var b=function(d){return parseInt(d,10)||0};var a=function(d){return !isNaN(parseInt(d,10))}})(jQuery);;
/*
 * jQuery UI Dialog 1.7.2
 *
 * Copyright (c) 2009 AUTHORS.txt (http://jqueryui.com/about)
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI/Dialog
 *
 * Depends:
 *	ui.core.js
 *	ui.draggable.js
 *	ui.resizable.js
 */
(function(c){var b={dragStart:"start.draggable",drag:"drag.draggable",dragStop:"stop.draggable",maxHeight:"maxHeight.resizable",minHeight:"minHeight.resizable",maxWidth:"maxWidth.resizable",minWidth:"minWidth.resizable",resizeStart:"start.resizable",resize:"drag.resizable",resizeStop:"stop.resizable"},a="ui-dialog ui-widget ui-widget-content ui-corner-all ";c.widget("ui.dialog",{_init:function(){this.originalTitle=this.element.attr("title");var l=this,m=this.options,j=m.title||this.originalTitle||"&nbsp;",e=c.ui.dialog.getTitleId(this.element),k=(this.uiDialog=c("<div/>")).appendTo(document.body).hide().addClass(a+m.dialogClass).css({position:"absolute",overflow:"hidden",zIndex:m.zIndex}).attr("tabIndex",-1).css("outline",0).keydown(function(n){(m.closeOnEscape&&n.keyCode&&n.keyCode==c.ui.keyCode.ESCAPE&&l.close(n))}).attr({role:"dialog","aria-labelledby":e}).mousedown(function(n){l.moveToTop(false,n)}),g=this.element.show().removeAttr("title").addClass("ui-dialog-content ui-widget-content").appendTo(k),f=(this.uiDialogTitlebar=c("<div></div>")).addClass("ui-dialog-titlebar ui-widget-header ui-corner-all ui-helper-clearfix").prependTo(k),i=c('<a href="#"/>').addClass("ui-dialog-titlebar-close ui-corner-all").attr("role","button").hover(function(){i.addClass("ui-state-hover")},function(){i.removeClass("ui-state-hover")}).focus(function(){i.addClass("ui-state-focus")}).blur(function(){i.removeClass("ui-state-focus")}).mousedown(function(n){n.stopPropagation()}).click(function(n){l.close(n);return false}).appendTo(f),h=(this.uiDialogTitlebarCloseText=c("<span/>")).addClass("ui-icon ui-icon-closethick").text(m.closeText).appendTo(i),d=c("<span/>").addClass("ui-dialog-title").attr("id",e).html(j).prependTo(f);f.find("*").add(f).disableSelection();(m.draggable&&c.fn.draggable&&this._makeDraggable());(m.resizable&&c.fn.resizable&&this._makeResizable());this._createButtons(m.buttons);this._isOpen=false;(m.bgiframe&&c.fn.bgiframe&&k.bgiframe());(m.autoOpen&&this.open())},destroy:function(){(this.overlay&&this.overlay.destroy());this.uiDialog.hide();this.element.unbind(".dialog").removeData("dialog").removeClass("ui-dialog-content ui-widget-content").hide().appendTo("body");this.uiDialog.remove();(this.originalTitle&&this.element.attr("title",this.originalTitle))},close:function(f){var d=this;if(false===d._trigger("beforeclose",f)){return}(d.overlay&&d.overlay.destroy());d.uiDialog.unbind("keypress.ui-dialog");(d.options.hide?d.uiDialog.hide(d.options.hide,function(){d._trigger("close",f)}):d.uiDialog.hide()&&d._trigger("close",f));c.ui.dialog.overlay.resize();d._isOpen=false;if(d.options.modal){var e=0;c(".ui-dialog").each(function(){if(this!=d.uiDialog[0]){e=Math.max(e,c(this).css("z-index"))}});c.ui.dialog.maxZ=e}},isOpen:function(){return this._isOpen},moveToTop:function(f,e){if((this.options.modal&&!f)||(!this.options.stack&&!this.options.modal)){return this._trigger("focus",e)}if(this.options.zIndex>c.ui.dialog.maxZ){c.ui.dialog.maxZ=this.options.zIndex}(this.overlay&&this.overlay.$el.css("z-index",c.ui.dialog.overlay.maxZ=++c.ui.dialog.maxZ));var d={scrollTop:this.element.attr("scrollTop"),scrollLeft:this.element.attr("scrollLeft")};this.uiDialog.css("z-index",++c.ui.dialog.maxZ);this.element.attr(d);this._trigger("focus",e)},open:function(){if(this._isOpen){return}var e=this.options,d=this.uiDialog;this.overlay=e.modal?new c.ui.dialog.overlay(this):null;(d.next().length&&d.appendTo("body"));this._size();this._position(e.position);d.show(e.show);this.moveToTop(true);(e.modal&&d.bind("keypress.ui-dialog",function(h){if(h.keyCode!=c.ui.keyCode.TAB){return}var g=c(":tabbable",this),i=g.filter(":first")[0],f=g.filter(":last")[0];if(h.target==f&&!h.shiftKey){setTimeout(function(){i.focus()},1)}else{if(h.target==i&&h.shiftKey){setTimeout(function(){f.focus()},1)}}}));c([]).add(d.find(".ui-dialog-content :tabbable:first")).add(d.find(".ui-dialog-buttonpane :tabbable:first")).add(d).filter(":first").focus();this._trigger("open");this._isOpen=true},_createButtons:function(g){var f=this,d=false,e=c("<div></div>").addClass("ui-dialog-buttonpane ui-widget-content ui-helper-clearfix");this.uiDialog.find(".ui-dialog-buttonpane").remove();(typeof g=="object"&&g!==null&&c.each(g,function(){return !(d=true)}));if(d){c.each(g,function(h,i){c('<button type="button"></button>').addClass("ui-state-default ui-corner-all").text(h).click(function(){i.apply(f.element[0],arguments)}).hover(function(){c(this).addClass("ui-state-hover")},function(){c(this).removeClass("ui-state-hover")}).focus(function(){c(this).addClass("ui-state-focus")}).blur(function(){c(this).removeClass("ui-state-focus")}).appendTo(e)});e.appendTo(this.uiDialog)}},_makeDraggable:function(){var d=this,f=this.options,e;this.uiDialog.draggable({cancel:".ui-dialog-content",handle:".ui-dialog-titlebar",containment:"document",start:function(){e=f.height;c(this).height(c(this).height()).addClass("ui-dialog-dragging");(f.dragStart&&f.dragStart.apply(d.element[0],arguments))},drag:function(){(f.drag&&f.drag.apply(d.element[0],arguments))},stop:function(){c(this).removeClass("ui-dialog-dragging").height(e);(f.dragStop&&f.dragStop.apply(d.element[0],arguments));c.ui.dialog.overlay.resize()}})},_makeResizable:function(g){g=(g===undefined?this.options.resizable:g);var d=this,f=this.options,e=typeof g=="string"?g:"n,e,s,w,se,sw,ne,nw";this.uiDialog.resizable({cancel:".ui-dialog-content",alsoResize:this.element,maxWidth:f.maxWidth,maxHeight:f.maxHeight,minWidth:f.minWidth,minHeight:f.minHeight,start:function(){c(this).addClass("ui-dialog-resizing");(f.resizeStart&&f.resizeStart.apply(d.element[0],arguments))},resize:function(){(f.resize&&f.resize.apply(d.element[0],arguments))},handles:e,stop:function(){c(this).removeClass("ui-dialog-resizing");f.height=c(this).height();f.width=c(this).width();(f.resizeStop&&f.resizeStop.apply(d.element[0],arguments));c.ui.dialog.overlay.resize()}}).find(".ui-resizable-se").addClass("ui-icon ui-icon-grip-diagonal-se")},_position:function(i){var e=c(window),f=c(document),g=f.scrollTop(),d=f.scrollLeft(),h=g;if(c.inArray(i,["center","top","right","bottom","left"])>=0){i=[i=="right"||i=="left"?i:"center",i=="top"||i=="bottom"?i:"middle"]}if(i.constructor!=Array){i=["center","middle"]}if(i[0].constructor==Number){d+=i[0]}else{switch(i[0]){case"left":d+=0;break;case"right":d+=e.width()-this.uiDialog.outerWidth();break;default:case"center":d+=(e.width()-this.uiDialog.outerWidth())/2}}if(i[1].constructor==Number){g+=i[1]}else{switch(i[1]){case"top":g+=0;break;case"bottom":g+=e.height()-this.uiDialog.outerHeight();break;default:case"middle":g+=(e.height()-this.uiDialog.outerHeight())/2}}g=Math.max(g,h);this.uiDialog.css({top:g,left:d})},_setData:function(e,f){(b[e]&&this.uiDialog.data(b[e],f));switch(e){case"buttons":this._createButtons(f);break;case"closeText":this.uiDialogTitlebarCloseText.text(f);break;case"dialogClass":this.uiDialog.removeClass(this.options.dialogClass).addClass(a+f);break;case"draggable":(f?this._makeDraggable():this.uiDialog.draggable("destroy"));break;case"height":this.uiDialog.height(f);break;case"position":this._position(f);break;case"resizable":var d=this.uiDialog,g=this.uiDialog.is(":data(resizable)");(g&&!f&&d.resizable("destroy"));(g&&typeof f=="string"&&d.resizable("option","handles",f));(g||this._makeResizable(f));break;case"title":c(".ui-dialog-title",this.uiDialogTitlebar).html(f||"&nbsp;");break;case"width":this.uiDialog.width(f);break}c.widget.prototype._setData.apply(this,arguments)},_size:function(){var e=this.options;this.element.css({height:0,minHeight:0,width:"auto"});var d=this.uiDialog.css({height:"auto",width:e.width}).height();this.element.css({minHeight:Math.max(e.minHeight-d,0),height:e.height=="auto"?"auto":Math.max(e.height-d,0)})}});c.extend(c.ui.dialog,{version:"1.7.2",defaults:{autoOpen:true,bgiframe:false,buttons:{},closeOnEscape:true,closeText:"close",dialogClass:"",draggable:true,hide:null,height:"auto",maxHeight:false,maxWidth:false,minHeight:150,minWidth:150,modal:false,position:"center",resizable:true,show:null,stack:true,title:"",width:300,zIndex:1000},getter:"isOpen",uuid:0,maxZ:0,getTitleId:function(d){return"ui-dialog-title-"+(d.attr("id")||++this.uuid)},overlay:function(d){this.$el=c.ui.dialog.overlay.create(d)}});c.extend(c.ui.dialog.overlay,{instances:[],maxZ:0,events:c.map("focus,mousedown,mouseup,keydown,keypress,click".split(","),function(d){return d+".dialog-overlay"}).join(" "),create:function(e){if(this.instances.length===0){setTimeout(function(){if(c.ui.dialog.overlay.instances.length){c(document).bind(c.ui.dialog.overlay.events,function(f){var g=c(f.target).parents(".ui-dialog").css("zIndex")||0;return(g>c.ui.dialog.overlay.maxZ)})}},1);c(document).bind("keydown.dialog-overlay",function(f){(e.options.closeOnEscape&&f.keyCode&&f.keyCode==c.ui.keyCode.ESCAPE&&e.close(f))});c(window).bind("resize.dialog-overlay",c.ui.dialog.overlay.resize)}var d=c("<div></div>").appendTo(document.body).addClass("ui-widget-overlay").css({width:this.width(),height:this.height()});(e.options.bgiframe&&c.fn.bgiframe&&d.bgiframe());this.instances.push(d);return d},destroy:function(d){this.instances.splice(c.inArray(this.instances,d),1);if(this.instances.length===0){c([document,window]).unbind(".dialog-overlay")}d.remove();var e=0;c.each(this.instances,function(){e=Math.max(e,this.css("z-index"))});this.maxZ=e},height:function(){if(c.browser.msie&&c.browser.version<7){var e=Math.max(document.documentElement.scrollHeight,document.body.scrollHeight);var d=Math.max(document.documentElement.offsetHeight,document.body.offsetHeight);if(e<d){return c(window).height()+"px"}else{return e+"px"}}else{return c(document).height()+"px"}},width:function(){if(c.browser.msie&&c.browser.version<7){var d=Math.max(document.documentElement.scrollWidth,document.body.scrollWidth);var e=Math.max(document.documentElement.offsetWidth,document.body.offsetWidth);if(d<e){return c(window).width()+"px"}else{return d+"px"}}else{return c(document).width()+"px"}},resize:function(){var d=c([]);c.each(c.ui.dialog.overlay.instances,function(){d=d.add(this)});d.css({width:0,height:0}).css({width:c.ui.dialog.overlay.width(),height:c.ui.dialog.overlay.height()})}});c.extend(c.ui.dialog.overlay.prototype,{destroy:function(){c.ui.dialog.overlay.destroy(this.$el)}})})(jQuery);;
/*
 * jQuery UI Tabs 1.7.2
 *
 * Copyright (c) 2009 AUTHORS.txt (http://jqueryui.com/about)
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI/Tabs
 *
 * Depends:
 *	ui.core.js
 */
(function(a){a.widget("ui.tabs",{_init:function(){if(this.options.deselectable!==undefined){this.options.collapsible=this.options.deselectable}this._tabify(true)},_setData:function(b,c){if(b=="selected"){if(this.options.collapsible&&c==this.options.selected){return}this.select(c)}else{this.options[b]=c;if(b=="deselectable"){this.options.collapsible=c}this._tabify()}},_tabId:function(b){return b.title&&b.title.replace(/\s/g,"_").replace(/[^A-Za-z0-9\-_:\.]/g,"")||this.options.idPrefix+a.data(b)},_sanitizeSelector:function(b){return b.replace(/:/g,"\\:")},_cookie:function(){var b=this.cookie||(this.cookie=this.options.cookie.name||"ui-tabs-"+a.data(this.list[0]));return a.cookie.apply(null,[b].concat(a.makeArray(arguments)))},_ui:function(c,b){return{tab:c,panel:b,index:this.anchors.index(c)}},_cleanup:function(){this.lis.filter(".ui-state-processing").removeClass("ui-state-processing").find("span:data(label.tabs)").each(function(){var b=a(this);b.html(b.data("label.tabs")).removeData("label.tabs")})},_tabify:function(n){this.list=this.element.children("ul:first");this.lis=a("li:has(a[href])",this.list);this.anchors=this.lis.map(function(){return a("a",this)[0]});this.panels=a([]);var p=this,d=this.options;var c=/^#.+/;this.anchors.each(function(r,o){var q=a(o).attr("href");var s=q.split("#")[0],u;if(s&&(s===location.toString().split("#")[0]||(u=a("base")[0])&&s===u.href)){q=o.hash;o.href=q}if(c.test(q)){p.panels=p.panels.add(p._sanitizeSelector(q))}else{if(q!="#"){a.data(o,"href.tabs",q);a.data(o,"load.tabs",q.replace(/#.*$/,""));var w=p._tabId(o);o.href="#"+w;var v=a("#"+w);if(!v.length){v=a(d.panelTemplate).attr("id",w).addClass("ui-tabs-panel ui-widget-content ui-corner-bottom").insertAfter(p.panels[r-1]||p.list);v.data("destroy.tabs",true)}p.panels=p.panels.add(v)}else{d.disabled.push(r)}}});if(n){this.element.addClass("ui-tabs ui-widget ui-widget-content ui-corner-all");this.list.addClass("ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all");this.lis.addClass("ui-state-default ui-corner-top");this.panels.addClass("ui-tabs-panel ui-widget-content ui-corner-bottom");if(d.selected===undefined){if(location.hash){this.anchors.each(function(q,o){if(o.hash==location.hash){d.selected=q;return false}})}if(typeof d.selected!="number"&&d.cookie){d.selected=parseInt(p._cookie(),10)}if(typeof d.selected!="number"&&this.lis.filter(".ui-tabs-selected").length){d.selected=this.lis.index(this.lis.filter(".ui-tabs-selected"))}d.selected=d.selected||0}else{if(d.selected===null){d.selected=-1}}d.selected=((d.selected>=0&&this.anchors[d.selected])||d.selected<0)?d.selected:0;d.disabled=a.unique(d.disabled.concat(a.map(this.lis.filter(".ui-state-disabled"),function(q,o){return p.lis.index(q)}))).sort();if(a.inArray(d.selected,d.disabled)!=-1){d.disabled.splice(a.inArray(d.selected,d.disabled),1)}this.panels.addClass("ui-tabs-hide");this.lis.removeClass("ui-tabs-selected ui-state-active");if(d.selected>=0&&this.anchors.length){this.panels.eq(d.selected).removeClass("ui-tabs-hide");this.lis.eq(d.selected).addClass("ui-tabs-selected ui-state-active");p.element.queue("tabs",function(){p._trigger("show",null,p._ui(p.anchors[d.selected],p.panels[d.selected]))});this.load(d.selected)}a(window).bind("unload",function(){p.lis.add(p.anchors).unbind(".tabs");p.lis=p.anchors=p.panels=null})}else{d.selected=this.lis.index(this.lis.filter(".ui-tabs-selected"))}this.element[d.collapsible?"addClass":"removeClass"]("ui-tabs-collapsible");if(d.cookie){this._cookie(d.selected,d.cookie)}for(var g=0,m;(m=this.lis[g]);g++){a(m)[a.inArray(g,d.disabled)!=-1&&!a(m).hasClass("ui-tabs-selected")?"addClass":"removeClass"]("ui-state-disabled")}if(d.cache===false){this.anchors.removeData("cache.tabs")}this.lis.add(this.anchors).unbind(".tabs");if(d.event!="mouseover"){var f=function(o,i){if(i.is(":not(.ui-state-disabled)")){i.addClass("ui-state-"+o)}};var j=function(o,i){i.removeClass("ui-state-"+o)};this.lis.bind("mouseover.tabs",function(){f("hover",a(this))});this.lis.bind("mouseout.tabs",function(){j("hover",a(this))});this.anchors.bind("focus.tabs",function(){f("focus",a(this).closest("li"))});this.anchors.bind("blur.tabs",function(){j("focus",a(this).closest("li"))})}var b,h;if(d.fx){if(a.isArray(d.fx)){b=d.fx[0];h=d.fx[1]}else{b=h=d.fx}}function e(i,o){i.css({display:""});if(a.browser.msie&&o.opacity){i[0].style.removeAttribute("filter")}}var k=h?function(i,o){a(i).closest("li").removeClass("ui-state-default").addClass("ui-tabs-selected ui-state-active");o.hide().removeClass("ui-tabs-hide").animate(h,h.duration||"normal",function(){e(o,h);p._trigger("show",null,p._ui(i,o[0]))})}:function(i,o){a(i).closest("li").removeClass("ui-state-default").addClass("ui-tabs-selected ui-state-active");o.removeClass("ui-tabs-hide");p._trigger("show",null,p._ui(i,o[0]))};var l=b?function(o,i){i.animate(b,b.duration||"normal",function(){p.lis.removeClass("ui-tabs-selected ui-state-active").addClass("ui-state-default");i.addClass("ui-tabs-hide");e(i,b);p.element.dequeue("tabs")})}:function(o,i,q){p.lis.removeClass("ui-tabs-selected ui-state-active").addClass("ui-state-default");i.addClass("ui-tabs-hide");p.element.dequeue("tabs")};this.anchors.bind(d.event+".tabs",function(){var o=this,r=a(this).closest("li"),i=p.panels.filter(":not(.ui-tabs-hide)"),q=a(p._sanitizeSelector(this.hash));if((r.hasClass("ui-tabs-selected")&&!d.collapsible)||r.hasClass("ui-state-disabled")||r.hasClass("ui-state-processing")||p._trigger("select",null,p._ui(this,q[0]))===false){this.blur();return false}d.selected=p.anchors.index(this);p.abort();if(d.collapsible){if(r.hasClass("ui-tabs-selected")){d.selected=-1;if(d.cookie){p._cookie(d.selected,d.cookie)}p.element.queue("tabs",function(){l(o,i)}).dequeue("tabs");this.blur();return false}else{if(!i.length){if(d.cookie){p._cookie(d.selected,d.cookie)}p.element.queue("tabs",function(){k(o,q)});p.load(p.anchors.index(this));this.blur();return false}}}if(d.cookie){p._cookie(d.selected,d.cookie)}if(q.length){if(i.length){p.element.queue("tabs",function(){l(o,i)})}p.element.queue("tabs",function(){k(o,q)});p.load(p.anchors.index(this))}else{throw"jQuery UI Tabs: Mismatching fragment identifier."}if(a.browser.msie){this.blur()}});this.anchors.bind("click.tabs",function(){return false})},destroy:function(){var b=this.options;this.abort();this.element.unbind(".tabs").removeClass("ui-tabs ui-widget ui-widget-content ui-corner-all ui-tabs-collapsible").removeData("tabs");this.list.removeClass("ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all");this.anchors.each(function(){var c=a.data(this,"href.tabs");if(c){this.href=c}var d=a(this).unbind(".tabs");a.each(["href","load","cache"],function(e,f){d.removeData(f+".tabs")})});this.lis.unbind(".tabs").add(this.panels).each(function(){if(a.data(this,"destroy.tabs")){a(this).remove()}else{a(this).removeClass(["ui-state-default","ui-corner-top","ui-tabs-selected","ui-state-active","ui-state-hover","ui-state-focus","ui-state-disabled","ui-tabs-panel","ui-widget-content","ui-corner-bottom","ui-tabs-hide"].join(" "))}});if(b.cookie){this._cookie(null,b.cookie)}},add:function(e,d,c){if(c===undefined){c=this.anchors.length}var b=this,g=this.options,i=a(g.tabTemplate.replace(/#\{href\}/g,e).replace(/#\{label\}/g,d)),h=!e.indexOf("#")?e.replace("#",""):this._tabId(a("a",i)[0]);i.addClass("ui-state-default ui-corner-top").data("destroy.tabs",true);var f=a("#"+h);if(!f.length){f=a(g.panelTemplate).attr("id",h).data("destroy.tabs",true)}f.addClass("ui-tabs-panel ui-widget-content ui-corner-bottom ui-tabs-hide");if(c>=this.lis.length){i.appendTo(this.list);f.appendTo(this.list[0].parentNode)}else{i.insertBefore(this.lis[c]);f.insertBefore(this.panels[c])}g.disabled=a.map(g.disabled,function(k,j){return k>=c?++k:k});this._tabify();if(this.anchors.length==1){i.addClass("ui-tabs-selected ui-state-active");f.removeClass("ui-tabs-hide");this.element.queue("tabs",function(){b._trigger("show",null,b._ui(b.anchors[0],b.panels[0]))});this.load(0)}this._trigger("add",null,this._ui(this.anchors[c],this.panels[c]))},remove:function(b){var d=this.options,e=this.lis.eq(b).remove(),c=this.panels.eq(b).remove();if(e.hasClass("ui-tabs-selected")&&this.anchors.length>1){this.select(b+(b+1<this.anchors.length?1:-1))}d.disabled=a.map(a.grep(d.disabled,function(g,f){return g!=b}),function(g,f){return g>=b?--g:g});this._tabify();this._trigger("remove",null,this._ui(e.find("a")[0],c[0]))},enable:function(b){var c=this.options;if(a.inArray(b,c.disabled)==-1){return}this.lis.eq(b).removeClass("ui-state-disabled");c.disabled=a.grep(c.disabled,function(e,d){return e!=b});this._trigger("enable",null,this._ui(this.anchors[b],this.panels[b]))},disable:function(c){var b=this,d=this.options;if(c!=d.selected){this.lis.eq(c).addClass("ui-state-disabled");d.disabled.push(c);d.disabled.sort();this._trigger("disable",null,this._ui(this.anchors[c],this.panels[c]))}},select:function(b){if(typeof b=="string"){b=this.anchors.index(this.anchors.filter("[href$="+b+"]"))}else{if(b===null){b=-1}}if(b==-1&&this.options.collapsible){b=this.options.selected}this.anchors.eq(b).trigger(this.options.event+".tabs")},load:function(e){var c=this,g=this.options,b=this.anchors.eq(e)[0],d=a.data(b,"load.tabs");this.abort();if(!d||this.element.queue("tabs").length!==0&&a.data(b,"cache.tabs")){this.element.dequeue("tabs");return}this.lis.eq(e).addClass("ui-state-processing");if(g.spinner){var f=a("span",b);f.data("label.tabs",f.html()).html(g.spinner)}this.xhr=a.ajax(a.extend({},g.ajaxOptions,{url:d,success:function(i,h){a(c._sanitizeSelector(b.hash)).html(i);c._cleanup();if(g.cache){a.data(b,"cache.tabs",true)}c._trigger("load",null,c._ui(c.anchors[e],c.panels[e]));try{g.ajaxOptions.success(i,h)}catch(j){}c.element.dequeue("tabs")}}))},abort:function(){this.element.queue([]);this.panels.stop(false,true);if(this.xhr){this.xhr.abort();delete this.xhr}this._cleanup()},url:function(c,b){this.anchors.eq(c).removeData("cache.tabs").data("load.tabs",b)},length:function(){return this.anchors.length}});a.extend(a.ui.tabs,{version:"1.7.2",getter:"length",defaults:{ajaxOptions:null,cache:false,cookie:null,collapsible:false,disabled:[],event:"click",fx:null,idPrefix:"ui-tabs-",panelTemplate:"<div></div>",spinner:"<em>Loading&#8230;</em>",tabTemplate:'<li><a href="#{href}"><span>#{label}</span></a></li>'}});a.extend(a.ui.tabs.prototype,{rotation:null,rotate:function(d,f){var b=this,g=this.options;var c=b._rotate||(b._rotate=function(h){clearTimeout(b.rotation);b.rotation=setTimeout(function(){var i=g.selected;b.select(++i<b.anchors.length?i:0)},d);if(h){h.stopPropagation()}});var e=b._unrotate||(b._unrotate=!f?function(h){if(h.clientX){b.rotate(null)}}:function(h){t=g.selected;c()});if(d){this.element.bind("tabsshow",c);this.anchors.bind(g.event+".tabs",e);c()}else{clearTimeout(b.rotation);this.element.unbind("tabsshow",c);this.anchors.unbind(g.event+".tabs",e);delete this._rotate;delete this._unrotate}}})})(jQuery);;/*
/*
 * jQuery UI Datepicker 1.7.2
 *
 * Copyright (c) 2009 AUTHORS.txt (http://jqueryui.com/about)
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI/Datepicker
 *
 * Depends:
 *	ui.core.js
 */
(function($){$.extend($.ui,{datepicker:{version:"1.7.2"}});var PROP_NAME="datepicker";function Datepicker(){this.debug=false;this._curInst=null;this._keyEvent=false;this._disabledInputs=[];this._datepickerShowing=false;this._inDialog=false;this._mainDivId="ui-datepicker-div";this._inlineClass="ui-datepicker-inline";this._appendClass="ui-datepicker-append";this._triggerClass="ui-datepicker-trigger";this._dialogClass="ui-datepicker-dialog";this._disableClass="ui-datepicker-disabled";this._unselectableClass="ui-datepicker-unselectable";this._currentClass="ui-datepicker-current-day";this._dayOverClass="ui-datepicker-days-cell-over";this.regional=[];this.regional[""]={closeText:"Done",prevText:"Prev",nextText:"Next",currentText:"Today",monthNames:["January","February","March","April","May","June","July","August","September","October","November","December"],monthNamesShort:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],dayNames:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],dayNamesShort:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],dayNamesMin:["Su","Mo","Tu","We","Th","Fr","Sa"],dateFormat:"mm/dd/yy",firstDay:0,isRTL:false};this._defaults={showOn:"focus",showAnim:"show",showOptions:{},defaultDate:null,appendText:"",buttonText:"...",buttonImage:"",buttonImageOnly:false,hideIfNoPrevNext:false,navigationAsDateFormat:false,gotoCurrent:false,changeMonth:false,changeYear:false,showMonthAfterYear:false,yearRange:"-10:+10",showOtherMonths:false,calculateWeek:this.iso8601Week,shortYearCutoff:"+10",minDate:null,maxDate:null,duration:"normal",beforeShowDay:null,beforeShow:null,onSelect:null,onChangeMonthYear:null,onClose:null,numberOfMonths:1,showCurrentAtPos:0,stepMonths:1,stepBigMonths:12,altField:"",altFormat:"",constrainInput:true,showButtonPanel:false};$.extend(this._defaults,this.regional[""]);this.dpDiv=$('<div id="'+this._mainDivId+'" class="ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all ui-helper-hidden-accessible"></div>')}$.extend(Datepicker.prototype,{markerClassName:"hasDatepicker",log:function(){if(this.debug){console.log.apply("",arguments)}},setDefaults:function(settings){extendRemove(this._defaults,settings||{});return this},_attachDatepicker:function(target,settings){var inlineSettings=null;for(var attrName in this._defaults){var attrValue=target.getAttribute("date:"+attrName);if(attrValue){inlineSettings=inlineSettings||{};try{inlineSettings[attrName]=eval(attrValue)}catch(err){inlineSettings[attrName]=attrValue}}}var nodeName=target.nodeName.toLowerCase();var inline=(nodeName=="div"||nodeName=="span");if(!target.id){target.id="dp"+(++this.uuid)}var inst=this._newInst($(target),inline);inst.settings=$.extend({},settings||{},inlineSettings||{});if(nodeName=="input"){this._connectDatepicker(target,inst)}else{if(inline){this._inlineDatepicker(target,inst)}}},_newInst:function(target,inline){var id=target[0].id.replace(/([:\[\]\.])/g,"\\\\$1");return{id:id,input:target,selectedDay:0,selectedMonth:0,selectedYear:0,drawMonth:0,drawYear:0,inline:inline,dpDiv:(!inline?this.dpDiv:$('<div class="'+this._inlineClass+' ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all"></div>'))}},_connectDatepicker:function(target,inst){var input=$(target);inst.append=$([]);inst.trigger=$([]);if(input.hasClass(this.markerClassName)){return}var appendText=this._get(inst,"appendText");var isRTL=this._get(inst,"isRTL");if(appendText){inst.append=$('<span class="'+this._appendClass+'">'+appendText+"</span>");input[isRTL?"before":"after"](inst.append)}var showOn=this._get(inst,"showOn");if(showOn=="focus"||showOn=="both"){input.focus(this._showDatepicker)}if(showOn=="button"||showOn=="both"){var buttonText=this._get(inst,"buttonText");var buttonImage=this._get(inst,"buttonImage");inst.trigger=$(this._get(inst,"buttonImageOnly")?$("<img/>").addClass(this._triggerClass).attr({src:buttonImage,alt:buttonText,title:buttonText}):$('<button type="button"></button>').addClass(this._triggerClass).html(buttonImage==""?buttonText:$("<img/>").attr({src:buttonImage,alt:buttonText,title:buttonText})));input[isRTL?"before":"after"](inst.trigger);inst.trigger.click(function(){if($.datepicker._datepickerShowing&&$.datepicker._lastInput==target){$.datepicker._hideDatepicker()}else{$.datepicker._showDatepicker(target)}return false})}input.addClass(this.markerClassName).keydown(this._doKeyDown).keypress(this._doKeyPress).bind("setData.datepicker",function(event,key,value){inst.settings[key]=value}).bind("getData.datepicker",function(event,key){return this._get(inst,key)});$.data(target,PROP_NAME,inst)},_inlineDatepicker:function(target,inst){var divSpan=$(target);if(divSpan.hasClass(this.markerClassName)){return}divSpan.addClass(this.markerClassName).append(inst.dpDiv).bind("setData.datepicker",function(event,key,value){inst.settings[key]=value}).bind("getData.datepicker",function(event,key){return this._get(inst,key)});$.data(target,PROP_NAME,inst);this._setDate(inst,this._getDefaultDate(inst));this._updateDatepicker(inst);this._updateAlternate(inst)},_dialogDatepicker:function(input,dateText,onSelect,settings,pos){var inst=this._dialogInst;if(!inst){var id="dp"+(++this.uuid);this._dialogInput=$('<input type="text" id="'+id+'" size="1" style="position: absolute; top: -100px;"/>');this._dialogInput.keydown(this._doKeyDown);$("body").append(this._dialogInput);inst=this._dialogInst=this._newInst(this._dialogInput,false);inst.settings={};$.data(this._dialogInput[0],PROP_NAME,inst)}extendRemove(inst.settings,settings||{});this._dialogInput.val(dateText);this._pos=(pos?(pos.length?pos:[pos.pageX,pos.pageY]):null);if(!this._pos){var browserWidth=window.innerWidth||document.documentElement.clientWidth||document.body.clientWidth;var browserHeight=window.innerHeight||document.documentElement.clientHeight||document.body.clientHeight;var scrollX=document.documentElement.scrollLeft||document.body.scrollLeft;var scrollY=document.documentElement.scrollTop||document.body.scrollTop;this._pos=[(browserWidth/2)-100+scrollX,(browserHeight/2)-150+scrollY]}this._dialogInput.css("left",this._pos[0]+"px").css("top",this._pos[1]+"px");inst.settings.onSelect=onSelect;this._inDialog=true;this.dpDiv.addClass(this._dialogClass);this._showDatepicker(this._dialogInput[0]);if($.blockUI){$.blockUI(this.dpDiv)}$.data(this._dialogInput[0],PROP_NAME,inst);return this},_destroyDatepicker:function(target){var $target=$(target);var inst=$.data(target,PROP_NAME);if(!$target.hasClass(this.markerClassName)){return}var nodeName=target.nodeName.toLowerCase();$.removeData(target,PROP_NAME);if(nodeName=="input"){inst.append.remove();inst.trigger.remove();$target.removeClass(this.markerClassName).unbind("focus",this._showDatepicker).unbind("keydown",this._doKeyDown).unbind("keypress",this._doKeyPress)}else{if(nodeName=="div"||nodeName=="span"){$target.removeClass(this.markerClassName).empty()}}},_enableDatepicker:function(target){var $target=$(target);var inst=$.data(target,PROP_NAME);if(!$target.hasClass(this.markerClassName)){return}var nodeName=target.nodeName.toLowerCase();if(nodeName=="input"){target.disabled=false;inst.trigger.filter("button").each(function(){this.disabled=false}).end().filter("img").css({opacity:"1.0",cursor:""})}else{if(nodeName=="div"||nodeName=="span"){var inline=$target.children("."+this._inlineClass);inline.children().removeClass("ui-state-disabled")}}this._disabledInputs=$.map(this._disabledInputs,function(value){return(value==target?null:value)})},_disableDatepicker:function(target){var $target=$(target);var inst=$.data(target,PROP_NAME);if(!$target.hasClass(this.markerClassName)){return}var nodeName=target.nodeName.toLowerCase();if(nodeName=="input"){target.disabled=true;inst.trigger.filter("button").each(function(){this.disabled=true}).end().filter("img").css({opacity:"0.5",cursor:"default"})}else{if(nodeName=="div"||nodeName=="span"){var inline=$target.children("."+this._inlineClass);inline.children().addClass("ui-state-disabled")}}this._disabledInputs=$.map(this._disabledInputs,function(value){return(value==target?null:value)});this._disabledInputs[this._disabledInputs.length]=target},_isDisabledDatepicker:function(target){if(!target){return false}for(var i=0;i<this._disabledInputs.length;i++){if(this._disabledInputs[i]==target){return true}}return false},_getInst:function(target){try{return $.data(target,PROP_NAME)}catch(err){throw"Missing instance data for this datepicker"}},_optionDatepicker:function(target,name,value){var inst=this._getInst(target);if(arguments.length==2&&typeof name=="string"){return(name=="defaults"?$.extend({},$.datepicker._defaults):(inst?(name=="all"?$.extend({},inst.settings):this._get(inst,name)):null))}var settings=name||{};if(typeof name=="string"){settings={};settings[name]=value}if(inst){if(this._curInst==inst){this._hideDatepicker(null)}var date=this._getDateDatepicker(target);extendRemove(inst.settings,settings);this._setDateDatepicker(target,date);this._updateDatepicker(inst)}},_changeDatepicker:function(target,name,value){this._optionDatepicker(target,name,value)},_refreshDatepicker:function(target){var inst=this._getInst(target);if(inst){this._updateDatepicker(inst)}},_setDateDatepicker:function(target,date,endDate){var inst=this._getInst(target);if(inst){this._setDate(inst,date,endDate);this._updateDatepicker(inst);this._updateAlternate(inst)}},_getDateDatepicker:function(target){var inst=this._getInst(target);if(inst&&!inst.inline){this._setDateFromField(inst)}return(inst?this._getDate(inst):null)},_doKeyDown:function(event){var inst=$.datepicker._getInst(event.target);var handled=true;var isRTL=inst.dpDiv.is(".ui-datepicker-rtl");inst._keyEvent=true;if($.datepicker._datepickerShowing){switch(event.keyCode){case 9:$.datepicker._hideDatepicker(null,"");break;case 13:var sel=$("td."+$.datepicker._dayOverClass+", td."+$.datepicker._currentClass,inst.dpDiv);if(sel[0]){$.datepicker._selectDay(event.target,inst.selectedMonth,inst.selectedYear,sel[0])}else{$.datepicker._hideDatepicker(null,$.datepicker._get(inst,"duration"))}return false;break;case 27:$.datepicker._hideDatepicker(null,$.datepicker._get(inst,"duration"));break;case 33:$.datepicker._adjustDate(event.target,(event.ctrlKey?-$.datepicker._get(inst,"stepBigMonths"):-$.datepicker._get(inst,"stepMonths")),"M");break;case 34:$.datepicker._adjustDate(event.target,(event.ctrlKey?+$.datepicker._get(inst,"stepBigMonths"):+$.datepicker._get(inst,"stepMonths")),"M");break;case 35:if(event.ctrlKey||event.metaKey){$.datepicker._clearDate(event.target)}handled=event.ctrlKey||event.metaKey;break;case 36:if(event.ctrlKey||event.metaKey){$.datepicker._gotoToday(event.target)}handled=event.ctrlKey||event.metaKey;break;case 37:if(event.ctrlKey||event.metaKey){$.datepicker._adjustDate(event.target,(isRTL?+1:-1),"D")}handled=event.ctrlKey||event.metaKey;if(event.originalEvent.altKey){$.datepicker._adjustDate(event.target,(event.ctrlKey?-$.datepicker._get(inst,"stepBigMonths"):-$.datepicker._get(inst,"stepMonths")),"M")}break;case 38:if(event.ctrlKey||event.metaKey){$.datepicker._adjustDate(event.target,-7,"D")}handled=event.ctrlKey||event.metaKey;break;case 39:if(event.ctrlKey||event.metaKey){$.datepicker._adjustDate(event.target,(isRTL?-1:+1),"D")}handled=event.ctrlKey||event.metaKey;if(event.originalEvent.altKey){$.datepicker._adjustDate(event.target,(event.ctrlKey?+$.datepicker._get(inst,"stepBigMonths"):+$.datepicker._get(inst,"stepMonths")),"M")}break;case 40:if(event.ctrlKey||event.metaKey){$.datepicker._adjustDate(event.target,+7,"D")}handled=event.ctrlKey||event.metaKey;break;default:handled=false}}else{if(event.keyCode==36&&event.ctrlKey){$.datepicker._showDatepicker(this)}else{handled=false}}if(handled){event.preventDefault();event.stopPropagation()}},_doKeyPress:function(event){var inst=$.datepicker._getInst(event.target);if($.datepicker._get(inst,"constrainInput")){var chars=$.datepicker._possibleChars($.datepicker._get(inst,"dateFormat"));var chr=String.fromCharCode(event.charCode==undefined?event.keyCode:event.charCode);return event.ctrlKey||(chr<" "||!chars||chars.indexOf(chr)>-1)}},_showDatepicker:function(input){input=input.target||input;if(input.nodeName.toLowerCase()!="input"){input=$("input",input.parentNode)[0]}if($.datepicker._isDisabledDatepicker(input)||$.datepicker._lastInput==input){return}var inst=$.datepicker._getInst(input);var beforeShow=$.datepicker._get(inst,"beforeShow");extendRemove(inst.settings,(beforeShow?beforeShow.apply(input,[input,inst]):{}));$.datepicker._hideDatepicker(null,"");$.datepicker._lastInput=input;$.datepicker._setDateFromField(inst);if($.datepicker._inDialog){input.value=""}if(!$.datepicker._pos){$.datepicker._pos=$.datepicker._findPos(input);$.datepicker._pos[1]+=input.offsetHeight}var isFixed=false;$(input).parents().each(function(){isFixed|=$(this).css("position")=="fixed";return !isFixed});if(isFixed&&$.browser.opera){$.datepicker._pos[0]-=document.documentElement.scrollLeft;$.datepicker._pos[1]-=document.documentElement.scrollTop}var offset={left:$.datepicker._pos[0],top:$.datepicker._pos[1]};$.datepicker._pos=null;inst.rangeStart=null;inst.dpDiv.css({position:"absolute",display:"block",top:"-1000px"});$.datepicker._updateDatepicker(inst);offset=$.datepicker._checkOffset(inst,offset,isFixed);inst.dpDiv.css({position:($.datepicker._inDialog&&$.blockUI?"static":(isFixed?"fixed":"absolute")),display:"none",left:offset.left+"px",top:offset.top+"px"});if(!inst.inline){var showAnim=$.datepicker._get(inst,"showAnim")||"show";var duration=$.datepicker._get(inst,"duration");var postProcess=function(){$.datepicker._datepickerShowing=true;if($.browser.msie&&parseInt($.browser.version,10)<7){$("iframe.ui-datepicker-cover").css({width:inst.dpDiv.width()+4,height:inst.dpDiv.height()+4})}};if($.effects&&$.effects[showAnim]){inst.dpDiv.show(showAnim,$.datepicker._get(inst,"showOptions"),duration,postProcess)}else{inst.dpDiv[showAnim](duration,postProcess)}if(duration==""){postProcess()}if(inst.input[0].type!="hidden"){inst.input[0].focus()}$.datepicker._curInst=inst}},_updateDatepicker:function(inst){var dims={width:inst.dpDiv.width()+4,height:inst.dpDiv.height()+4};var self=this;inst.dpDiv.empty().append(this._generateHTML(inst)).find("iframe.ui-datepicker-cover").css({width:dims.width,height:dims.height}).end().find("button, .ui-datepicker-prev, .ui-datepicker-next, .ui-datepicker-calendar td a").bind("mouseout",function(){$(this).removeClass("ui-state-hover");if(this.className.indexOf("ui-datepicker-prev")!=-1){$(this).removeClass("ui-datepicker-prev-hover")}if(this.className.indexOf("ui-datepicker-next")!=-1){$(this).removeClass("ui-datepicker-next-hover")}}).bind("mouseover",function(){if(!self._isDisabledDatepicker(inst.inline?inst.dpDiv.parent()[0]:inst.input[0])){$(this).parents(".ui-datepicker-calendar").find("a").removeClass("ui-state-hover");$(this).addClass("ui-state-hover");if(this.className.indexOf("ui-datepicker-prev")!=-1){$(this).addClass("ui-datepicker-prev-hover")}if(this.className.indexOf("ui-datepicker-next")!=-1){$(this).addClass("ui-datepicker-next-hover")}}}).end().find("."+this._dayOverClass+" a").trigger("mouseover").end();var numMonths=this._getNumberOfMonths(inst);var cols=numMonths[1];var width=17;if(cols>1){inst.dpDiv.addClass("ui-datepicker-multi-"+cols).css("width",(width*cols)+"em")}else{inst.dpDiv.removeClass("ui-datepicker-multi-2 ui-datepicker-multi-3 ui-datepicker-multi-4").width("")}inst.dpDiv[(numMonths[0]!=1||numMonths[1]!=1?"add":"remove")+"Class"]("ui-datepicker-multi");inst.dpDiv[(this._get(inst,"isRTL")?"add":"remove")+"Class"]("ui-datepicker-rtl");if(inst.input&&inst.input[0].type!="hidden"&&inst==$.datepicker._curInst){$(inst.input[0]).focus()}},_checkOffset:function(inst,offset,isFixed){var dpWidth=inst.dpDiv.outerWidth();var dpHeight=inst.dpDiv.outerHeight();var inputWidth=inst.input?inst.input.outerWidth():0;var inputHeight=inst.input?inst.input.outerHeight():0;var viewWidth=(window.innerWidth||document.documentElement.clientWidth||document.body.clientWidth)+$(document).scrollLeft();var viewHeight=(window.innerHeight||document.documentElement.clientHeight||document.body.clientHeight)+$(document).scrollTop();offset.left-=(this._get(inst,"isRTL")?(dpWidth-inputWidth):0);offset.left-=(isFixed&&offset.left==inst.input.offset().left)?$(document).scrollLeft():0;offset.top-=(isFixed&&offset.top==(inst.input.offset().top+inputHeight))?$(document).scrollTop():0;offset.left-=(offset.left+dpWidth>viewWidth&&viewWidth>dpWidth)?Math.abs(offset.left+dpWidth-viewWidth):0;offset.top-=(offset.top+dpHeight>viewHeight&&viewHeight>dpHeight)?Math.abs(offset.top+dpHeight+inputHeight*2-viewHeight):0;return offset},_findPos:function(obj){while(obj&&(obj.type=="hidden"||obj.nodeType!=1)){obj=obj.nextSibling}var position=$(obj).offset();return[position.left,position.top]},_hideDatepicker:function(input,duration){var inst=this._curInst;if(!inst||(input&&inst!=$.data(input,PROP_NAME))){return}if(inst.stayOpen){this._selectDate("#"+inst.id,this._formatDate(inst,inst.currentDay,inst.currentMonth,inst.currentYear))}inst.stayOpen=false;if(this._datepickerShowing){duration=(duration!=null?duration:this._get(inst,"duration"));var showAnim=this._get(inst,"showAnim");var postProcess=function(){$.datepicker._tidyDialog(inst)};if(duration!=""&&$.effects&&$.effects[showAnim]){inst.dpDiv.hide(showAnim,$.datepicker._get(inst,"showOptions"),duration,postProcess)}else{inst.dpDiv[(duration==""?"hide":(showAnim=="slideDown"?"slideUp":(showAnim=="fadeIn"?"fadeOut":"hide")))](duration,postProcess)}if(duration==""){this._tidyDialog(inst)}var onClose=this._get(inst,"onClose");if(onClose){onClose.apply((inst.input?inst.input[0]:null),[(inst.input?inst.input.val():""),inst])}this._datepickerShowing=false;this._lastInput=null;if(this._inDialog){this._dialogInput.css({position:"absolute",left:"0",top:"-100px"});if($.blockUI){$.unblockUI();$("body").append(this.dpDiv)}}this._inDialog=false}this._curInst=null},_tidyDialog:function(inst){inst.dpDiv.removeClass(this._dialogClass).unbind(".ui-datepicker-calendar")},_checkExternalClick:function(event){if(!$.datepicker._curInst){return}var $target=$(event.target);if(($target.parents("#"+$.datepicker._mainDivId).length==0)&&!$target.hasClass($.datepicker.markerClassName)&&!$target.hasClass($.datepicker._triggerClass)&&$.datepicker._datepickerShowing&&!($.datepicker._inDialog&&$.blockUI)){$.datepicker._hideDatepicker(null,"")}},_adjustDate:function(id,offset,period){var target=$(id);var inst=this._getInst(target[0]);if(this._isDisabledDatepicker(target[0])){return}this._adjustInstDate(inst,offset+(period=="M"?this._get(inst,"showCurrentAtPos"):0),period);this._updateDatepicker(inst)},_gotoToday:function(id){var target=$(id);var inst=this._getInst(target[0]);if(this._get(inst,"gotoCurrent")&&inst.currentDay){inst.selectedDay=inst.currentDay;inst.drawMonth=inst.selectedMonth=inst.currentMonth;inst.drawYear=inst.selectedYear=inst.currentYear}else{var date=new Date();inst.selectedDay=date.getDate();inst.drawMonth=inst.selectedMonth=date.getMonth();inst.drawYear=inst.selectedYear=date.getFullYear()}this._notifyChange(inst);this._adjustDate(target)},_selectMonthYear:function(id,select,period){var target=$(id);var inst=this._getInst(target[0]);inst._selectingMonthYear=false;inst["selected"+(period=="M"?"Month":"Year")]=inst["draw"+(period=="M"?"Month":"Year")]=parseInt(select.options[select.selectedIndex].value,10);this._notifyChange(inst);this._adjustDate(target)},_clickMonthYear:function(id){var target=$(id);var inst=this._getInst(target[0]);if(inst.input&&inst._selectingMonthYear&&!$.browser.msie){inst.input[0].focus()}inst._selectingMonthYear=!inst._selectingMonthYear},_selectDay:function(id,month,year,td){var target=$(id);if($(td).hasClass(this._unselectableClass)||this._isDisabledDatepicker(target[0])){return}var inst=this._getInst(target[0]);inst.selectedDay=inst.currentDay=$("a",td).html();inst.selectedMonth=inst.currentMonth=month;inst.selectedYear=inst.currentYear=year;if(inst.stayOpen){inst.endDay=inst.endMonth=inst.endYear=null}this._selectDate(id,this._formatDate(inst,inst.currentDay,inst.currentMonth,inst.currentYear));if(inst.stayOpen){inst.rangeStart=this._daylightSavingAdjust(new Date(inst.currentYear,inst.currentMonth,inst.currentDay));this._updateDatepicker(inst)}},_clearDate:function(id){var target=$(id);var inst=this._getInst(target[0]);inst.stayOpen=false;inst.endDay=inst.endMonth=inst.endYear=inst.rangeStart=null;this._selectDate(target,"")},_selectDate:function(id,dateStr){var target=$(id);var inst=this._getInst(target[0]);dateStr=(dateStr!=null?dateStr:this._formatDate(inst));if(inst.input){inst.input.val(dateStr)}this._updateAlternate(inst);var onSelect=this._get(inst,"onSelect");if(onSelect){onSelect.apply((inst.input?inst.input[0]:null),[dateStr,inst])}else{if(inst.input){inst.input.trigger("change")}}if(inst.inline){this._updateDatepicker(inst)}else{if(!inst.stayOpen){this._hideDatepicker(null,this._get(inst,"duration"));this._lastInput=inst.input[0];if(typeof(inst.input[0])!="object"){inst.input[0].focus()}this._lastInput=null}}},_updateAlternate:function(inst){var altField=this._get(inst,"altField");if(altField){var altFormat=this._get(inst,"altFormat")||this._get(inst,"dateFormat");var date=this._getDate(inst);dateStr=this.formatDate(altFormat,date,this._getFormatConfig(inst));$(altField).each(function(){$(this).val(dateStr)})}},noWeekends:function(date){var day=date.getDay();return[(day>0&&day<6),""]},iso8601Week:function(date){var checkDate=new Date(date.getFullYear(),date.getMonth(),date.getDate());var firstMon=new Date(checkDate.getFullYear(),1-1,4);var firstDay=firstMon.getDay()||7;firstMon.setDate(firstMon.getDate()+1-firstDay);if(firstDay<4&&checkDate<firstMon){checkDate.setDate(checkDate.getDate()-3);return $.datepicker.iso8601Week(checkDate)}else{if(checkDate>new Date(checkDate.getFullYear(),12-1,28)){firstDay=new Date(checkDate.getFullYear()+1,1-1,4).getDay()||7;if(firstDay>4&&(checkDate.getDay()||7)<firstDay-3){return 1}}}return Math.floor(((checkDate-firstMon)/86400000)/7)+1},parseDate:function(format,value,settings){if(format==null||value==null){throw"Invalid arguments"}value=(typeof value=="object"?value.toString():value+"");if(value==""){return null}var shortYearCutoff=(settings?settings.shortYearCutoff:null)||this._defaults.shortYearCutoff;var dayNamesShort=(settings?settings.dayNamesShort:null)||this._defaults.dayNamesShort;var dayNames=(settings?settings.dayNames:null)||this._defaults.dayNames;var monthNamesShort=(settings?settings.monthNamesShort:null)||this._defaults.monthNamesShort;var monthNames=(settings?settings.monthNames:null)||this._defaults.monthNames;var year=-1;var month=-1;var day=-1;var doy=-1;var literal=false;var lookAhead=function(match){var matches=(iFormat+1<format.length&&format.charAt(iFormat+1)==match);if(matches){iFormat++}return matches};var getNumber=function(match){lookAhead(match);var origSize=(match=="@"?14:(match=="y"?4:(match=="o"?3:2)));var size=origSize;var num=0;while(size>0&&iValue<value.length&&value.charAt(iValue)>="0"&&value.charAt(iValue)<="9"){num=num*10+parseInt(value.charAt(iValue++),10);size--}if(size==origSize){throw"Missing number at position "+iValue}return num};var getName=function(match,shortNames,longNames){var names=(lookAhead(match)?longNames:shortNames);var size=0;for(var j=0;j<names.length;j++){size=Math.max(size,names[j].length)}var name="";var iInit=iValue;while(size>0&&iValue<value.length){name+=value.charAt(iValue++);for(var i=0;i<names.length;i++){if(name==names[i]){return i+1}}size--}throw"Unknown name at position "+iInit};var checkLiteral=function(){if(value.charAt(iValue)!=format.charAt(iFormat)){throw"Unexpected literal at position "+iValue}iValue++};var iValue=0;for(var iFormat=0;iFormat<format.length;iFormat++){if(literal){if(format.charAt(iFormat)=="'"&&!lookAhead("'")){literal=false}else{checkLiteral()}}else{switch(format.charAt(iFormat)){case"d":day=getNumber("d");break;case"D":getName("D",dayNamesShort,dayNames);break;case"o":doy=getNumber("o");break;case"m":month=getNumber("m");break;case"M":month=getName("M",monthNamesShort,monthNames);break;case"y":year=getNumber("y");break;case"@":var date=new Date(getNumber("@"));year=date.getFullYear();month=date.getMonth()+1;day=date.getDate();break;case"'":if(lookAhead("'")){checkLiteral()}else{literal=true}break;default:checkLiteral()}}}if(year==-1){year=new Date().getFullYear()}else{if(year<100){year+=new Date().getFullYear()-new Date().getFullYear()%100+(year<=shortYearCutoff?0:-100)}}if(doy>-1){month=1;day=doy;do{var dim=this._getDaysInMonth(year,month-1);if(day<=dim){break}month++;day-=dim}while(true)}var date=this._daylightSavingAdjust(new Date(year,month-1,day));if(date.getFullYear()!=year||date.getMonth()+1!=month||date.getDate()!=day){throw"Invalid date"}return date},ATOM:"yy-mm-dd",COOKIE:"D, dd M yy",ISO_8601:"yy-mm-dd",RFC_822:"D, d M y",RFC_850:"DD, dd-M-y",RFC_1036:"D, d M y",RFC_1123:"D, d M yy",RFC_2822:"D, d M yy",RSS:"D, d M y",TIMESTAMP:"@",W3C:"yy-mm-dd",formatDate:function(format,date,settings){if(!date){return""}var dayNamesShort=(settings?settings.dayNamesShort:null)||this._defaults.dayNamesShort;var dayNames=(settings?settings.dayNames:null)||this._defaults.dayNames;var monthNamesShort=(settings?settings.monthNamesShort:null)||this._defaults.monthNamesShort;var monthNames=(settings?settings.monthNames:null)||this._defaults.monthNames;var lookAhead=function(match){var matches=(iFormat+1<format.length&&format.charAt(iFormat+1)==match);if(matches){iFormat++}return matches};var formatNumber=function(match,value,len){var num=""+value;if(lookAhead(match)){while(num.length<len){num="0"+num}}return num};var formatName=function(match,value,shortNames,longNames){return(lookAhead(match)?longNames[value]:shortNames[value])};var output="";var literal=false;if(date){for(var iFormat=0;iFormat<format.length;iFormat++){if(literal){if(format.charAt(iFormat)=="'"&&!lookAhead("'")){literal=false}else{output+=format.charAt(iFormat)}}else{switch(format.charAt(iFormat)){case"d":output+=formatNumber("d",date.getDate(),2);break;case"D":output+=formatName("D",date.getDay(),dayNamesShort,dayNames);break;case"o":var doy=date.getDate();for(var m=date.getMonth()-1;m>=0;m--){doy+=this._getDaysInMonth(date.getFullYear(),m)}output+=formatNumber("o",doy,3);break;case"m":output+=formatNumber("m",date.getMonth()+1,2);break;case"M":output+=formatName("M",date.getMonth(),monthNamesShort,monthNames);break;case"y":output+=(lookAhead("y")?date.getFullYear():(date.getYear()%100<10?"0":"")+date.getYear()%100);break;case"@":output+=date.getTime();break;case"'":if(lookAhead("'")){output+="'"}else{literal=true}break;default:output+=format.charAt(iFormat)}}}}return output},_possibleChars:function(format){var chars="";var literal=false;for(var iFormat=0;iFormat<format.length;iFormat++){if(literal){if(format.charAt(iFormat)=="'"&&!lookAhead("'")){literal=false}else{chars+=format.charAt(iFormat)}}else{switch(format.charAt(iFormat)){case"d":case"m":case"y":case"@":chars+="0123456789";break;case"D":case"M":return null;case"'":if(lookAhead("'")){chars+="'"}else{literal=true}break;default:chars+=format.charAt(iFormat)}}}return chars},_get:function(inst,name){return inst.settings[name]!==undefined?inst.settings[name]:this._defaults[name]},_setDateFromField:function(inst){var dateFormat=this._get(inst,"dateFormat");var dates=inst.input?inst.input.val():null;inst.endDay=inst.endMonth=inst.endYear=null;var date=defaultDate=this._getDefaultDate(inst);var settings=this._getFormatConfig(inst);try{date=this.parseDate(dateFormat,dates,settings)||defaultDate}catch(event){this.log(event);date=defaultDate}inst.selectedDay=date.getDate();inst.drawMonth=inst.selectedMonth=date.getMonth();inst.drawYear=inst.selectedYear=date.getFullYear();inst.currentDay=(dates?date.getDate():0);inst.currentMonth=(dates?date.getMonth():0);inst.currentYear=(dates?date.getFullYear():0);this._adjustInstDate(inst)},_getDefaultDate:function(inst){var date=this._determineDate(this._get(inst,"defaultDate"),new Date());var minDate=this._getMinMaxDate(inst,"min",true);var maxDate=this._getMinMaxDate(inst,"max");date=(minDate&&date<minDate?minDate:date);date=(maxDate&&date>maxDate?maxDate:date);return date},_determineDate:function(date,defaultDate){var offsetNumeric=function(offset){var date=new Date();date.setDate(date.getDate()+offset);return date};var offsetString=function(offset,getDaysInMonth){var date=new Date();var year=date.getFullYear();var month=date.getMonth();var day=date.getDate();var pattern=/([+-]?[0-9]+)\s*(d|D|w|W|m|M|y|Y)?/g;var matches=pattern.exec(offset);while(matches){switch(matches[2]||"d"){case"d":case"D":day+=parseInt(matches[1],10);break;case"w":case"W":day+=parseInt(matches[1],10)*7;break;case"m":case"M":month+=parseInt(matches[1],10);day=Math.min(day,getDaysInMonth(year,month));break;case"y":case"Y":year+=parseInt(matches[1],10);day=Math.min(day,getDaysInMonth(year,month));break}matches=pattern.exec(offset)}return new Date(year,month,day)};date=(date==null?defaultDate:(typeof date=="string"?offsetString(date,this._getDaysInMonth):(typeof date=="number"?(isNaN(date)?defaultDate:offsetNumeric(date)):date)));date=(date&&date.toString()=="Invalid Date"?defaultDate:date);if(date){date.setHours(0);date.setMinutes(0);date.setSeconds(0);date.setMilliseconds(0)}return this._daylightSavingAdjust(date)},_daylightSavingAdjust:function(date){if(!date){return null}date.setHours(date.getHours()>12?date.getHours()+2:0);return date},_setDate:function(inst,date,endDate){var clear=!(date);var origMonth=inst.selectedMonth;var origYear=inst.selectedYear;date=this._determineDate(date,new Date());inst.selectedDay=inst.currentDay=date.getDate();inst.drawMonth=inst.selectedMonth=inst.currentMonth=date.getMonth();inst.drawYear=inst.selectedYear=inst.currentYear=date.getFullYear();if(origMonth!=inst.selectedMonth||origYear!=inst.selectedYear){this._notifyChange(inst)}this._adjustInstDate(inst);if(inst.input){inst.input.val(clear?"":this._formatDate(inst))}},_getDate:function(inst){var startDate=(!inst.currentYear||(inst.input&&inst.input.val()=="")?null:this._daylightSavingAdjust(new Date(inst.currentYear,inst.currentMonth,inst.currentDay)));return startDate},_generateHTML:function(inst){var today=new Date();today=this._daylightSavingAdjust(new Date(today.getFullYear(),today.getMonth(),today.getDate()));var isRTL=this._get(inst,"isRTL");var showButtonPanel=this._get(inst,"showButtonPanel");var hideIfNoPrevNext=this._get(inst,"hideIfNoPrevNext");var navigationAsDateFormat=this._get(inst,"navigationAsDateFormat");var numMonths=this._getNumberOfMonths(inst);var showCurrentAtPos=this._get(inst,"showCurrentAtPos");var stepMonths=this._get(inst,"stepMonths");var stepBigMonths=this._get(inst,"stepBigMonths");var isMultiMonth=(numMonths[0]!=1||numMonths[1]!=1);var currentDate=this._daylightSavingAdjust((!inst.currentDay?new Date(9999,9,9):new Date(inst.currentYear,inst.currentMonth,inst.currentDay)));var minDate=this._getMinMaxDate(inst,"min",true);var maxDate=this._getMinMaxDate(inst,"max");var drawMonth=inst.drawMonth-showCurrentAtPos;var drawYear=inst.drawYear;if(drawMonth<0){drawMonth+=12;drawYear--}if(maxDate){var maxDraw=this._daylightSavingAdjust(new Date(maxDate.getFullYear(),maxDate.getMonth()-numMonths[1]+1,maxDate.getDate()));maxDraw=(minDate&&maxDraw<minDate?minDate:maxDraw);while(this._daylightSavingAdjust(new Date(drawYear,drawMonth,1))>maxDraw){drawMonth--;if(drawMonth<0){drawMonth=11;drawYear--}}}inst.drawMonth=drawMonth;inst.drawYear=drawYear;var prevText=this._get(inst,"prevText");prevText=(!navigationAsDateFormat?prevText:this.formatDate(prevText,this._daylightSavingAdjust(new Date(drawYear,drawMonth-stepMonths,1)),this._getFormatConfig(inst)));var prev=(this._canAdjustMonth(inst,-1,drawYear,drawMonth)?'<a class="ui-datepicker-prev ui-corner-all" onclick="DP_jQuery.datepicker._adjustDate(\'#'+inst.id+"', -"+stepMonths+", 'M');\" title=\""+prevText+'"><span class="ui-icon ui-icon-circle-triangle-'+(isRTL?"e":"w")+'">'+prevText+"</span></a>":(hideIfNoPrevNext?"":'<a class="ui-datepicker-prev ui-corner-all ui-state-disabled" title="'+prevText+'"><span class="ui-icon ui-icon-circle-triangle-'+(isRTL?"e":"w")+'">'+prevText+"</span></a>"));var nextText=this._get(inst,"nextText");nextText=(!navigationAsDateFormat?nextText:this.formatDate(nextText,this._daylightSavingAdjust(new Date(drawYear,drawMonth+stepMonths,1)),this._getFormatConfig(inst)));var next=(this._canAdjustMonth(inst,+1,drawYear,drawMonth)?'<a class="ui-datepicker-next ui-corner-all" onclick="DP_jQuery.datepicker._adjustDate(\'#'+inst.id+"', +"+stepMonths+", 'M');\" title=\""+nextText+'"><span class="ui-icon ui-icon-circle-triangle-'+(isRTL?"w":"e")+'">'+nextText+"</span></a>":(hideIfNoPrevNext?"":'<a class="ui-datepicker-next ui-corner-all ui-state-disabled" title="'+nextText+'"><span class="ui-icon ui-icon-circle-triangle-'+(isRTL?"w":"e")+'">'+nextText+"</span></a>"));var currentText=this._get(inst,"currentText");var gotoDate=(this._get(inst,"gotoCurrent")&&inst.currentDay?currentDate:today);currentText=(!navigationAsDateFormat?currentText:this.formatDate(currentText,gotoDate,this._getFormatConfig(inst)));var controls=(!inst.inline?'<button type="button" class="ui-datepicker-close ui-state-default ui-priority-primary ui-corner-all" onclick="DP_jQuery.datepicker._hideDatepicker();">'+this._get(inst,"closeText")+"</button>":"");var buttonPanel=(showButtonPanel)?'<div class="ui-datepicker-buttonpane ui-widget-content">'+(isRTL?controls:"")+(this._isInRange(inst,gotoDate)?'<button type="button" class="ui-datepicker-current ui-state-default ui-priority-secondary ui-corner-all" onclick="DP_jQuery.datepicker._gotoToday(\'#'+inst.id+"');\">"+currentText+"</button>":"")+(isRTL?"":controls)+"</div>":"";var firstDay=parseInt(this._get(inst,"firstDay"),10);firstDay=(isNaN(firstDay)?0:firstDay);var dayNames=this._get(inst,"dayNames");var dayNamesShort=this._get(inst,"dayNamesShort");var dayNamesMin=this._get(inst,"dayNamesMin");var monthNames=this._get(inst,"monthNames");var monthNamesShort=this._get(inst,"monthNamesShort");var beforeShowDay=this._get(inst,"beforeShowDay");var showOtherMonths=this._get(inst,"showOtherMonths");var calculateWeek=this._get(inst,"calculateWeek")||this.iso8601Week;var endDate=inst.endDay?this._daylightSavingAdjust(new Date(inst.endYear,inst.endMonth,inst.endDay)):currentDate;var defaultDate=this._getDefaultDate(inst);var html="";for(var row=0;row<numMonths[0];row++){var group="";for(var col=0;col<numMonths[1];col++){var selectedDate=this._daylightSavingAdjust(new Date(drawYear,drawMonth,inst.selectedDay));var cornerClass=" ui-corner-all";var calender="";if(isMultiMonth){calender+='<div class="ui-datepicker-group ui-datepicker-group-';switch(col){case 0:calender+="first";cornerClass=" ui-corner-"+(isRTL?"right":"left");break;case numMonths[1]-1:calender+="last";cornerClass=" ui-corner-"+(isRTL?"left":"right");break;default:calender+="middle";cornerClass="";break}calender+='">'}calender+='<div class="ui-datepicker-header ui-widget-header ui-helper-clearfix'+cornerClass+'">'+(/all|left/.test(cornerClass)&&row==0?(isRTL?next:prev):"")+(/all|right/.test(cornerClass)&&row==0?(isRTL?prev:next):"")+this._generateMonthYearHeader(inst,drawMonth,drawYear,minDate,maxDate,selectedDate,row>0||col>0,monthNames,monthNamesShort)+'</div><table class="ui-datepicker-calendar"><thead><tr>';var thead="";for(var dow=0;dow<7;dow++){var day=(dow+firstDay)%7;thead+="<th"+((dow+firstDay+6)%7>=5?' class="ui-datepicker-week-end"':"")+'><span title="'+dayNames[day]+'">'+dayNamesMin[day]+"</span></th>"}calender+=thead+"</tr></thead><tbody>";var daysInMonth=this._getDaysInMonth(drawYear,drawMonth);if(drawYear==inst.selectedYear&&drawMonth==inst.selectedMonth){inst.selectedDay=Math.min(inst.selectedDay,daysInMonth)}var leadDays=(this._getFirstDayOfMonth(drawYear,drawMonth)-firstDay+7)%7;var numRows=(isMultiMonth?6:Math.ceil((leadDays+daysInMonth)/7));var printDate=this._daylightSavingAdjust(new Date(drawYear,drawMonth,1-leadDays));for(var dRow=0;dRow<numRows;dRow++){calender+="<tr>";var tbody="";for(var dow=0;dow<7;dow++){var daySettings=(beforeShowDay?beforeShowDay.apply((inst.input?inst.input[0]:null),[printDate]):[true,""]);var otherMonth=(printDate.getMonth()!=drawMonth);var unselectable=otherMonth||!daySettings[0]||(minDate&&printDate<minDate)||(maxDate&&printDate>maxDate);tbody+='<td class="'+((dow+firstDay+6)%7>=5?" ui-datepicker-week-end":"")+(otherMonth?" ui-datepicker-other-month":"")+((printDate.getTime()==selectedDate.getTime()&&drawMonth==inst.selectedMonth&&inst._keyEvent)||(defaultDate.getTime()==printDate.getTime()&&defaultDate.getTime()==selectedDate.getTime())?" "+this._dayOverClass:"")+(unselectable?" "+this._unselectableClass+" ui-state-disabled":"")+(otherMonth&&!showOtherMonths?"":" "+daySettings[1]+(printDate.getTime()>=currentDate.getTime()&&printDate.getTime()<=endDate.getTime()?" "+this._currentClass:"")+(printDate.getTime()==today.getTime()?" ui-datepicker-today":""))+'"'+((!otherMonth||showOtherMonths)&&daySettings[2]?' title="'+daySettings[2]+'"':"")+(unselectable?"":" onclick=\"DP_jQuery.datepicker._selectDay('#"+inst.id+"',"+drawMonth+","+drawYear+', this);return false;"')+">"+(otherMonth?(showOtherMonths?printDate.getDate():"&#xa0;"):(unselectable?'<span class="ui-state-default">'+printDate.getDate()+"</span>":'<a class="ui-state-default'+(printDate.getTime()==today.getTime()?" ui-state-highlight":"")+(printDate.getTime()>=currentDate.getTime()&&printDate.getTime()<=endDate.getTime()?" ui-state-active":"")+'" href="#">'+printDate.getDate()+"</a>"))+"</td>";printDate.setDate(printDate.getDate()+1);printDate=this._daylightSavingAdjust(printDate)}calender+=tbody+"</tr>"}drawMonth++;if(drawMonth>11){drawMonth=0;drawYear++}calender+="</tbody></table>"+(isMultiMonth?"</div>"+((numMonths[0]>0&&col==numMonths[1]-1)?'<div class="ui-datepicker-row-break"></div>':""):"");group+=calender}html+=group}html+=buttonPanel+($.browser.msie&&parseInt($.browser.version,10)<7&&!inst.inline?'<iframe src="javascript:false;" class="ui-datepicker-cover" frameborder="0"></iframe>':"");inst._keyEvent=false;return html},_generateMonthYearHeader:function(inst,drawMonth,drawYear,minDate,maxDate,selectedDate,secondary,monthNames,monthNamesShort){minDate=(inst.rangeStart&&minDate&&selectedDate<minDate?selectedDate:minDate);var changeMonth=this._get(inst,"changeMonth");var changeYear=this._get(inst,"changeYear");var showMonthAfterYear=this._get(inst,"showMonthAfterYear");var html='<div class="ui-datepicker-title">';var monthHtml="";if(secondary||!changeMonth){monthHtml+='<span class="ui-datepicker-month">'+monthNames[drawMonth]+"</span> "}else{var inMinYear=(minDate&&minDate.getFullYear()==drawYear);var inMaxYear=(maxDate&&maxDate.getFullYear()==drawYear);monthHtml+='<select class="ui-datepicker-month" onchange="DP_jQuery.datepicker._selectMonthYear(\'#'+inst.id+"', this, 'M');\" onclick=\"DP_jQuery.datepicker._clickMonthYear('#"+inst.id+"');\">";for(var month=0;month<12;month++){if((!inMinYear||month>=minDate.getMonth())&&(!inMaxYear||month<=maxDate.getMonth())){monthHtml+='<option value="'+month+'"'+(month==drawMonth?' selected="selected"':"")+">"+monthNamesShort[month]+"</option>"}}monthHtml+="</select>"}if(!showMonthAfterYear){html+=monthHtml+((secondary||changeMonth||changeYear)&&(!(changeMonth&&changeYear))?"&#xa0;":"")}if(secondary||!changeYear){html+='<span class="ui-datepicker-year">'+drawYear+"</span>"}else{var years=this._get(inst,"yearRange").split(":");var year=0;var endYear=0;if(years.length!=2){year=drawYear-10;endYear=drawYear+10}else{if(years[0].charAt(0)=="+"||years[0].charAt(0)=="-"){year=drawYear+parseInt(years[0],10);endYear=drawYear+parseInt(years[1],10)}else{year=parseInt(years[0],10);endYear=parseInt(years[1],10)}}year=(minDate?Math.max(year,minDate.getFullYear()):year);endYear=(maxDate?Math.min(endYear,maxDate.getFullYear()):endYear);html+='<select class="ui-datepicker-year" onchange="DP_jQuery.datepicker._selectMonthYear(\'#'+inst.id+"', this, 'Y');\" onclick=\"DP_jQuery.datepicker._clickMonthYear('#"+inst.id+"');\">";for(;year<=endYear;year++){html+='<option value="'+year+'"'+(year==drawYear?' selected="selected"':"")+">"+year+"</option>"}html+="</select>"}if(showMonthAfterYear){html+=(secondary||changeMonth||changeYear?"&#xa0;":"")+monthHtml}html+="</div>";return html},_adjustInstDate:function(inst,offset,period){var year=inst.drawYear+(period=="Y"?offset:0);var month=inst.drawMonth+(period=="M"?offset:0);var day=Math.min(inst.selectedDay,this._getDaysInMonth(year,month))+(period=="D"?offset:0);var date=this._daylightSavingAdjust(new Date(year,month,day));var minDate=this._getMinMaxDate(inst,"min",true);var maxDate=this._getMinMaxDate(inst,"max");date=(minDate&&date<minDate?minDate:date);date=(maxDate&&date>maxDate?maxDate:date);inst.selectedDay=date.getDate();inst.drawMonth=inst.selectedMonth=date.getMonth();inst.drawYear=inst.selectedYear=date.getFullYear();if(period=="M"||period=="Y"){this._notifyChange(inst)}},_notifyChange:function(inst){var onChange=this._get(inst,"onChangeMonthYear");if(onChange){onChange.apply((inst.input?inst.input[0]:null),[inst.selectedYear,inst.selectedMonth+1,inst])}},_getNumberOfMonths:function(inst){var numMonths=this._get(inst,"numberOfMonths");return(numMonths==null?[1,1]:(typeof numMonths=="number"?[1,numMonths]:numMonths))},_getMinMaxDate:function(inst,minMax,checkRange){var date=this._determineDate(this._get(inst,minMax+"Date"),null);return(!checkRange||!inst.rangeStart?date:(!date||inst.rangeStart>date?inst.rangeStart:date))},_getDaysInMonth:function(year,month){return 32-new Date(year,month,32).getDate()},_getFirstDayOfMonth:function(year,month){return new Date(year,month,1).getDay()},_canAdjustMonth:function(inst,offset,curYear,curMonth){var numMonths=this._getNumberOfMonths(inst);var date=this._daylightSavingAdjust(new Date(curYear,curMonth+(offset<0?offset:numMonths[1]),1));if(offset<0){date.setDate(this._getDaysInMonth(date.getFullYear(),date.getMonth()))}return this._isInRange(inst,date)},_isInRange:function(inst,date){var newMinDate=(!inst.rangeStart?null:this._daylightSavingAdjust(new Date(inst.selectedYear,inst.selectedMonth,inst.selectedDay)));newMinDate=(newMinDate&&inst.rangeStart<newMinDate?inst.rangeStart:newMinDate);var minDate=newMinDate||this._getMinMaxDate(inst,"min");var maxDate=this._getMinMaxDate(inst,"max");return((!minDate||date>=minDate)&&(!maxDate||date<=maxDate))},_getFormatConfig:function(inst){var shortYearCutoff=this._get(inst,"shortYearCutoff");shortYearCutoff=(typeof shortYearCutoff!="string"?shortYearCutoff:new Date().getFullYear()%100+parseInt(shortYearCutoff,10));return{shortYearCutoff:shortYearCutoff,dayNamesShort:this._get(inst,"dayNamesShort"),dayNames:this._get(inst,"dayNames"),monthNamesShort:this._get(inst,"monthNamesShort"),monthNames:this._get(inst,"monthNames")}},_formatDate:function(inst,day,month,year){if(!day){inst.currentDay=inst.selectedDay;inst.currentMonth=inst.selectedMonth;inst.currentYear=inst.selectedYear}var date=(day?(typeof day=="object"?day:this._daylightSavingAdjust(new Date(year,month,day))):this._daylightSavingAdjust(new Date(inst.currentYear,inst.currentMonth,inst.currentDay)));return this.formatDate(this._get(inst,"dateFormat"),date,this._getFormatConfig(inst))}});function extendRemove(target,props){$.extend(target,props);for(var name in props){if(props[name]==null||props[name]==undefined){target[name]=props[name]}}return target}function isArray(a){return(a&&(($.browser.safari&&typeof a=="object"&&a.length)||(a.constructor&&a.constructor.toString().match(/\Array\(\)/))))}$.fn.datepicker=function(options){if(!$.datepicker.initialized){$(document).mousedown($.datepicker._checkExternalClick).find("body").append($.datepicker.dpDiv);$.datepicker.initialized=true}var otherArgs=Array.prototype.slice.call(arguments,1);if(typeof options=="string"&&(options=="isDisabled"||options=="getDate")){return $.datepicker["_"+options+"Datepicker"].apply($.datepicker,[this[0]].concat(otherArgs))}if(options=="option"&&arguments.length==2&&typeof arguments[1]=="string"){return $.datepicker["_"+options+"Datepicker"].apply($.datepicker,[this[0]].concat(otherArgs))}return this.each(function(){typeof options=="string"?$.datepicker["_"+options+"Datepicker"].apply($.datepicker,[this].concat(otherArgs)):$.datepicker._attachDatepicker(this,options)})};$.datepicker=new Datepicker();$.datepicker.initialized=false;$.datepicker.uuid=new Date().getTime();$.datepicker.version="1.7.2";window.DP_jQuery=$})(jQuery);;
/*
 * jQuery Form Plugin
 * version: 2.36 (07-NOV-2009)
 * @requires jQuery v1.2.6 or later
 *
 * Examples and documentation at: http://malsup.com/jquery/form/
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 */
;(function($) {

/*
	Usage Note:
	-----------
	Do not use both ajaxSubmit and ajaxForm on the same form.  These
	functions are intended to be exclusive.  Use ajaxSubmit if you want
	to bind your own submit handler to the form.  For example,

	$(document).ready(function() {
		$('#myForm').bind('submit', function() {
			$(this).ajaxSubmit({
				target: '#output'
			});
			return false; // <-- important!
		});
	});

	Use ajaxForm when you want the plugin to manage all the event binding
	for you.  For example,

	$(document).ready(function() {
		$('#myForm').ajaxForm({
			target: '#output'
		});
	});

	When using ajaxForm, the ajaxSubmit function will be invoked for you
	at the appropriate time.
*/

/**
 * ajaxSubmit() provides a mechanism for immediately submitting
 * an HTML form using AJAX.
 */
$.fn.ajaxSubmit = function(options) {
	// fast fail if nothing selected (http://dev.jquery.com/ticket/2752)
	if (!this.length) {
		log('ajaxSubmit: skipping submit process - no element selected');
		return this;
	}

	if (typeof options == 'function')
		options = { success: options };

	var url = $.trim(this.attr('action'));
	if (url) {
		// clean url (don't include hash vaue)
		url = (url.match(/^([^#]+)/)||[])[1];
   	}
   	url = url || window.location.href || '';

	options = $.extend({
		url:  url,
		type: this.attr('method') || 'GET',
		iframeSrc: /^https/i.test(window.location.href || '') ? 'javascript:false' : 'about:blank'
	}, options || {});

	// hook for manipulating the form data before it is extracted;
	// convenient for use with rich editors like tinyMCE or FCKEditor
	var veto = {};
	this.trigger('form-pre-serialize', [this, options, veto]);
	if (veto.veto) {
		log('ajaxSubmit: submit vetoed via form-pre-serialize trigger');
		return this;
	}

	// provide opportunity to alter form data before it is serialized
	if (options.beforeSerialize && options.beforeSerialize(this, options) === false) {
		log('ajaxSubmit: submit aborted via beforeSerialize callback');
		return this;
	}

	var a = this.formToArray(options.semantic);
	if (options.data) {
		options.extraData = options.data;
		for (var n in options.data) {
		  if(options.data[n] instanceof Array) {
			for (var k in options.data[n])
			  a.push( { name: n, value: options.data[n][k] } );
		  }
		  else
			 a.push( { name: n, value: options.data[n] } );
		}
	}

	// give pre-submit callback an opportunity to abort the submit
	if (options.beforeSubmit && options.beforeSubmit(a, this, options) === false) {
		log('ajaxSubmit: submit aborted via beforeSubmit callback');
		return this;
	}

	// fire vetoable 'validate' event
	this.trigger('form-submit-validate', [a, this, options, veto]);
	if (veto.veto) {
		log('ajaxSubmit: submit vetoed via form-submit-validate trigger');
		return this;
	}

	var q = $.param(a);

	if (options.type.toUpperCase() == 'GET') {
		options.url += (options.url.indexOf('?') >= 0 ? '&' : '?') + q;
		options.data = null;  // data is null for 'get'
	}
	else
		options.data = q; // data is the query string for 'post'

	var $form = this, callbacks = [];
	if (options.resetForm) callbacks.push(function() { $form.resetForm(); });
	if (options.clearForm) callbacks.push(function() { $form.clearForm(); });

	// perform a load on the target only if dataType is not provided
	if (!options.dataType && options.target) {
		var oldSuccess = options.success || function(){};
		callbacks.push(function(data) {
			$(options.target).html(data).each(oldSuccess, arguments);
		});
	}
	else if (options.success)
		callbacks.push(options.success);

	options.success = function(data, status) {
		for (var i=0, max=callbacks.length; i < max; i++)
			callbacks[i].apply(options, [data, status, $form]);
	};

	// are there files to upload?
	var files = $('input:file', this).fieldValue();
	var found = false;
	for (var j=0; j < files.length; j++)
		if (files[j])
			found = true;

	var multipart = false;
//	var mp = 'multipart/form-data';
//	multipart = ($form.attr('enctype') == mp || $form.attr('encoding') == mp);

	// options.iframe allows user to force iframe mode
	// 06-NOV-09: now defaulting to iframe mode if file input is detected
   if ((files.length && options.iframe !== false) || options.iframe || found || multipart) {
	   // hack to fix Safari hang (thanks to Tim Molendijk for this)
	   // see:  http://groups.google.com/group/jquery-dev/browse_thread/thread/36395b7ab510dd5d
	   if (options.closeKeepAlive)
		   $.get(options.closeKeepAlive, fileUpload);
	   else
		   fileUpload();
	   }
   else
	   $.ajax(options);

	// fire 'notify' event
	this.trigger('form-submit-notify', [this, options]);
	return this;


	// private function for handling file uploads (hat tip to YAHOO!)
	function fileUpload() {
		var form = $form[0];

		if ($(':input[name=submit]', form).length) {
			alert('Error: Form elements must not be named "submit".');
			return;
		}

		var opts = $.extend({}, $.ajaxSettings, options);
		var s = $.extend(true, {}, $.extend(true, {}, $.ajaxSettings), opts);

		var id = 'jqFormIO' + (new Date().getTime());
		var $io = $('<iframe id="' + id + '" name="' + id + '" src="'+ opts.iframeSrc +'" />');
		var io = $io[0];

		$io.css({ position: 'absolute', top: '-1000px', left: '-1000px' });

		var xhr = { // mock object
			aborted: 0,
			responseText: null,
			responseXML: null,
			status: 0,
			statusText: 'n/a',
			getAllResponseHeaders: function() {},
			getResponseHeader: function() {},
			setRequestHeader: function() {},
			abort: function() {
				this.aborted = 1;
				$io.attr('src', opts.iframeSrc); // abort op in progress
			}
		};

		var g = opts.global;
		// trigger ajax global events so that activity/block indicators work like normal
		if (g && ! $.active++) $.event.trigger("ajaxStart");
		if (g) $.event.trigger("ajaxSend", [xhr, opts]);

		if (s.beforeSend && s.beforeSend(xhr, s) === false) {
			s.global && $.active--;
			return;
		}
		if (xhr.aborted)
			return;

		var cbInvoked = 0;
		var timedOut = 0;

		// add submitting element to data if we know it
		var sub = form.clk;
		if (sub) {
			var n = sub.name;
			if (n && !sub.disabled) {
				options.extraData = options.extraData || {};
				options.extraData[n] = sub.value;
				if (sub.type == "image") {
					options.extraData[name+'.x'] = form.clk_x;
					options.extraData[name+'.y'] = form.clk_y;
				}
			}
		}

		// take a breath so that pending repaints get some cpu time before the upload starts
		setTimeout(function() {
			// make sure form attrs are set
			var t = $form.attr('target'), a = $form.attr('action');

			// update form attrs in IE friendly way
			form.setAttribute('target',id);
			if (form.getAttribute('method') != 'POST')
				form.setAttribute('method', 'POST');
			if (form.getAttribute('action') != opts.url)
				form.setAttribute('action', opts.url);

			// ie borks in some cases when setting encoding
			if (! options.skipEncodingOverride) {
				$form.attr({
					encoding: 'multipart/form-data',
					enctype:  'multipart/form-data'
				});
			}

			// support timout
			if (opts.timeout)
				setTimeout(function() { timedOut = true; cb(); }, opts.timeout);

			// add "extra" data to form if provided in options
			var extraInputs = [];
			try {
				if (options.extraData)
					for (var n in options.extraData)
						extraInputs.push(
							$('<input type="hidden" name="'+n+'" value="'+options.extraData[n]+'" />')
								.appendTo(form)[0]);

				// add iframe to doc and submit the form
				$io.appendTo('body');
				io.attachEvent ? io.attachEvent('onload', cb) : io.addEventListener('load', cb, false);
				form.submit();
			}
			finally {
				// reset attrs and remove "extra" input elements
				form.setAttribute('action',a);
				t ? form.setAttribute('target', t) : $form.removeAttr('target');
				$(extraInputs).remove();
			}
		}, 10);

		var domCheckCount = 50;

		function cb() {
			if (cbInvoked++) return;

			io.detachEvent ? io.detachEvent('onload', cb) : io.removeEventListener('load', cb, false);

			var ok = true;
			try {
				if (timedOut) throw 'timeout';
				// extract the server response from the iframe
				var data, doc;

				doc = io.contentWindow ? io.contentWindow.document : io.contentDocument ? io.contentDocument : io.document;
				
				var isXml = opts.dataType == 'xml' || doc.XMLDocument || $.isXMLDoc(doc);
				log('isXml='+isXml);
				if (!isXml && (doc.body == null || doc.body.innerHTML == '')) {
				 	if (--domCheckCount) {
						// in some browsers (Opera) the iframe DOM is not always traversable when
						// the onload callback fires, so we loop a bit to accommodate
						cbInvoked = 0;
						setTimeout(cb, 100);
						return;
					}
					log('Could not access iframe DOM after 50 tries.');
					return;
				}

				xhr.responseText = doc.body ? doc.body.innerHTML : null;
				xhr.responseXML = doc.XMLDocument ? doc.XMLDocument : doc;
				xhr.getResponseHeader = function(header){
					var headers = {'content-type': opts.dataType};
					return headers[header];
				};

				if (opts.dataType == 'json' || opts.dataType == 'script') {
					// see if user embedded response in textarea
					var ta = doc.getElementsByTagName('textarea')[0];
					if (ta)
						xhr.responseText = ta.value;
					else {
						// account for browsers injecting pre around json response
						var pre = doc.getElementsByTagName('pre')[0];
						if (pre)
							xhr.responseText = pre.innerHTML;
					}			  
				}
				else if (opts.dataType == 'xml' && !xhr.responseXML && xhr.responseText != null) {
					xhr.responseXML = toXml(xhr.responseText);
				}
				data = $.httpData(xhr, opts.dataType);
			}
			catch(e){
				ok = false;
				$.handleError(opts, xhr, 'error', e);
			}

			// ordering of these callbacks/triggers is odd, but that's how $.ajax does it
			if (ok) {
				opts.success(data, 'success');
				if (g) $.event.trigger("ajaxSuccess", [xhr, opts]);
			}
			if (g) $.event.trigger("ajaxComplete", [xhr, opts]);
			if (g && ! --$.active) $.event.trigger("ajaxStop");
			if (opts.complete) opts.complete(xhr, ok ? 'success' : 'error');

			// clean up
			setTimeout(function() {
				$io.remove();
				xhr.responseXML = null;
			}, 100);
		};

		function toXml(s, doc) {
			if (window.ActiveXObject) {
				doc = new ActiveXObject('Microsoft.XMLDOM');
				doc.async = 'false';
				doc.loadXML(s);
			}
			else
				doc = (new DOMParser()).parseFromString(s, 'text/xml');
			return (doc && doc.documentElement && doc.documentElement.tagName != 'parsererror') ? doc : null;
		};
	};
};

/**
 * ajaxForm() provides a mechanism for fully automating form submission.
 *
 * The advantages of using this method instead of ajaxSubmit() are:
 *
 * 1: This method will include coordinates for <input type="image" /> elements (if the element
 *	is used to submit the form).
 * 2. This method will include the submit element's name/value data (for the element that was
 *	used to submit the form).
 * 3. This method binds the submit() method to the form for you.
 *
 * The options argument for ajaxForm works exactly as it does for ajaxSubmit.  ajaxForm merely
 * passes the options argument along after properly binding events for submit elements and
 * the form itself.
 */
$.fn.ajaxForm = function(options) {
	return this.ajaxFormUnbind().bind('submit.form-plugin', function() {
		$(this).ajaxSubmit(options);
		return false;
	}).bind('click.form-plugin', function(e) {
		var target = e.target;
		var $el = $(target);
		if (!($el.is(":submit,input:image"))) {
			// is this a child element of the submit el?  (ex: a span within a button)
			var t = $el.closest(':submit');
			if (t.length == 0)
				return;
			target = t[0];
		}
		var form = this;
		form.clk = target;
		if (target.type == 'image') {
			if (e.offsetX != undefined) {
				form.clk_x = e.offsetX;
				form.clk_y = e.offsetY;
			} else if (typeof $.fn.offset == 'function') { // try to use dimensions plugin
				var offset = $el.offset();
				form.clk_x = e.pageX - offset.left;
				form.clk_y = e.pageY - offset.top;
			} else {
				form.clk_x = e.pageX - target.offsetLeft;
				form.clk_y = e.pageY - target.offsetTop;
			}
		}
		// clear form vars
		setTimeout(function() { form.clk = form.clk_x = form.clk_y = null; }, 100);
	});
};

// ajaxFormUnbind unbinds the event handlers that were bound by ajaxForm
$.fn.ajaxFormUnbind = function() {
	return this.unbind('submit.form-plugin click.form-plugin');
};

/**
 * formToArray() gathers form element data into an array of objects that can
 * be passed to any of the following ajax functions: $.get, $.post, or load.
 * Each object in the array has both a 'name' and 'value' property.  An example of
 * an array for a simple login form might be:
 *
 * [ { name: 'username', value: 'jresig' }, { name: 'password', value: 'secret' } ]
 *
 * It is this array that is passed to pre-submit callback functions provided to the
 * ajaxSubmit() and ajaxForm() methods.
 */
$.fn.formToArray = function(semantic) {
	var a = [];
	if (this.length == 0) return a;

	var form = this[0];
	var els = semantic ? form.getElementsByTagName('*') : form.elements;
	if (!els) return a;
	for(var i=0, max=els.length; i < max; i++) {
		var el = els[i];
		var n = el.name;
		if (!n) continue;

		if (semantic && form.clk && el.type == "image") {
			// handle image inputs on the fly when semantic == true
			if(!el.disabled && form.clk == el) {
				a.push({name: n, value: $(el).val()});
				a.push({name: n+'.x', value: form.clk_x}, {name: n+'.y', value: form.clk_y});
			}
			continue;
		}

		var v = $.fieldValue(el, true);
		if (v && v.constructor == Array) {
			for(var j=0, jmax=v.length; j < jmax; j++)
				a.push({name: n, value: v[j]});
		}
		else if (v !== null && typeof v != 'undefined')
			a.push({name: n, value: v});
	}

	if (!semantic && form.clk) {
		// input type=='image' are not found in elements array! handle it here
		var $input = $(form.clk), input = $input[0], n = input.name;
		if (n && !input.disabled && input.type == 'image') {
			a.push({name: n, value: $input.val()});
			a.push({name: n+'.x', value: form.clk_x}, {name: n+'.y', value: form.clk_y});
		}
	}
	return a;
};

/**
 * Serializes form data into a 'submittable' string. This method will return a string
 * in the format: name1=value1&amp;name2=value2
 */
$.fn.formSerialize = function(semantic) {
	//hand off to jQuery.param for proper encoding
	return $.param(this.formToArray(semantic));
};

/**
 * Serializes all field elements in the jQuery object into a query string.
 * This method will return a string in the format: name1=value1&amp;name2=value2
 */
$.fn.fieldSerialize = function(successful) {
	var a = [];
	this.each(function() {
		var n = this.name;
		if (!n) return;
		var v = $.fieldValue(this, successful);
		if (v && v.constructor == Array) {
			for (var i=0,max=v.length; i < max; i++)
				a.push({name: n, value: v[i]});
		}
		else if (v !== null && typeof v != 'undefined')
			a.push({name: this.name, value: v});
	});
	//hand off to jQuery.param for proper encoding
	return $.param(a);
};

/**
 * Returns the value(s) of the element in the matched set.  For example, consider the following form:
 *
 *  <form><fieldset>
 *	  <input name="A" type="text" />
 *	  <input name="A" type="text" />
 *	  <input name="B" type="checkbox" value="B1" />
 *	  <input name="B" type="checkbox" value="B2"/>
 *	  <input name="C" type="radio" value="C1" />
 *	  <input name="C" type="radio" value="C2" />
 *  </fieldset></form>
 *
 *  var v = $(':text').fieldValue();
 *  // if no values are entered into the text inputs
 *  v == ['','']
 *  // if values entered into the text inputs are 'foo' and 'bar'
 *  v == ['foo','bar']
 *
 *  var v = $(':checkbox').fieldValue();
 *  // if neither checkbox is checked
 *  v === undefined
 *  // if both checkboxes are checked
 *  v == ['B1', 'B2']
 *
 *  var v = $(':radio').fieldValue();
 *  // if neither radio is checked
 *  v === undefined
 *  // if first radio is checked
 *  v == ['C1']
 *
 * The successful argument controls whether or not the field element must be 'successful'
 * (per http://www.w3.org/TR/html4/interact/forms.html#successful-controls).
 * The default value of the successful argument is true.  If this value is false the value(s)
 * for each element is returned.
 *
 * Note: This method *always* returns an array.  If no valid value can be determined the
 *	   array will be empty, otherwise it will contain one or more values.
 */
$.fn.fieldValue = function(successful) {
	for (var val=[], i=0, max=this.length; i < max; i++) {
		var el = this[i];
		var v = $.fieldValue(el, successful);
		if (v === null || typeof v == 'undefined' || (v.constructor == Array && !v.length))
			continue;
		v.constructor == Array ? $.merge(val, v) : val.push(v);
	}
	return val;
};

/**
 * Returns the value of the field element.
 */
$.fieldValue = function(el, successful) {
	var n = el.name, t = el.type, tag = el.tagName.toLowerCase();
	if (typeof successful == 'undefined') successful = true;

	if (successful && (!n || el.disabled || t == 'reset' || t == 'button' ||
		(t == 'checkbox' || t == 'radio') && !el.checked ||
		(t == 'submit' || t == 'image') && el.form && el.form.clk != el ||
		tag == 'select' && el.selectedIndex == -1))
			return null;

	if (tag == 'select') {
		var index = el.selectedIndex;
		if (index < 0) return null;
		var a = [], ops = el.options;
		var one = (t == 'select-one');
		var max = (one ? index+1 : ops.length);
		for(var i=(one ? index : 0); i < max; i++) {
			var op = ops[i];
			if (op.selected) {
				var v = op.value;
				if (!v) // extra pain for IE...
					v = (op.attributes && op.attributes['value'] && !(op.attributes['value'].specified)) ? op.text : op.value;
				if (one) return v;
				a.push(v);
			}
		}
		return a;
	}
	return el.value;
};

/**
 * Clears the form data.  Takes the following actions on the form's input fields:
 *  - input text fields will have their 'value' property set to the empty string
 *  - select elements will have their 'selectedIndex' property set to -1
 *  - checkbox and radio inputs will have their 'checked' property set to false
 *  - inputs of type submit, button, reset, and hidden will *not* be effected
 *  - button elements will *not* be effected
 */
$.fn.clearForm = function() {
	return this.each(function() {
		$('input,select,textarea', this).clearFields();
	});
};

/**
 * Clears the selected form elements.
 */
$.fn.clearFields = $.fn.clearInputs = function() {
	return this.each(function() {
		var t = this.type, tag = this.tagName.toLowerCase();
		if (t == 'text' || t == 'password' || tag == 'textarea')
			this.value = '';
		else if (t == 'checkbox' || t == 'radio')
			this.checked = false;
		else if (tag == 'select')
			this.selectedIndex = -1;
	});
};

/**
 * Resets the form data.  Causes all form elements to be reset to their original value.
 */
$.fn.resetForm = function() {
	return this.each(function() {
		// guard against an input with the name of 'reset'
		// note that IE reports the reset function as an 'object'
		if (typeof this.reset == 'function' || (typeof this.reset == 'object' && !this.reset.nodeType))
			this.reset();
	});
};

/**
 * Enables or disables any matching elements.
 */
$.fn.enable = function(b) {
	if (b == undefined) b = true;
	return this.each(function() {
		this.disabled = !b;
	});
};

/**
 * Checks/unchecks any matching checkboxes or radio buttons and
 * selects/deselects and matching option elements.
 */
$.fn.selected = function(select) {
	if (select == undefined) select = true;
	return this.each(function() {
		var t = this.type;
		if (t == 'checkbox' || t == 'radio')
			this.checked = select;
		else if (this.tagName.toLowerCase() == 'option') {
			var $sel = $(this).parent('select');
			if (select && $sel[0] && $sel[0].type == 'select-one') {
				// deselect all other options
				$sel.find('option').selected(false);
			}
			this.selected = select;
		}
	});
};

// helper fn for console logging
// set $.fn.ajaxSubmit.debug to true to enable debug logging
function log() {
	if ($.fn.ajaxSubmit.debug && window.console && window.console.log)
		window.console.log('[jquery.form] ' + Array.prototype.join.call(arguments,''));
};

})(jQuery);

/*
 * jQuery validation plug-in 1.6
 *
 * http://bassistance.de/jquery-plugins/jquery-plugin-validation/
 * http://docs.jquery.com/Plugins/Validation
 *
 * Copyright (c) 2006 - 2008 JÃ¶rn Zaefferer
 *
 * $Id: jquery.validate.js 6403 2009-06-17 14:27:16Z joern.zaefferer $
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 */

(function($) {

$.extend($.fn, {
	// http://docs.jquery.com/Plugins/Validation/validate
	validate: function( options ) {

		// if nothing is selected, return nothing; can't chain anyway
		if (!this.length) {
			options && options.debug && window.console && console.warn( "nothing selected, can't validate, returning nothing" );
			return;
		}

		// check if a validator for this form was already created
		var validator = $.data(this[0], 'validator');
		if ( validator ) {
			return validator;
		}
		
		validator = new $.validator( options, this[0] );
		$.data(this[0], 'validator', validator); 
		
		if ( validator.settings.onsubmit ) {
		
			// allow suppresing validation by adding a cancel class to the submit button
			this.find("input, button").filter(".cancel").click(function() {
				validator.cancelSubmit = true;
			});
			
			// when a submitHandler is used, capture the submitting button
			if (validator.settings.submitHandler) {
				this.find("input, button").filter(":submit").click(function() {
					validator.submitButton = this;
				});
			}
		
			// validate the form on submit
			this.submit( function( event ) {
				if ( validator.settings.debug )
					// prevent form submit to be able to see console output
					event.preventDefault();
					
				function handle() {
					if ( validator.settings.submitHandler ) {
						if (validator.submitButton) {
							// insert a hidden input as a replacement for the missing submit button
							var hidden = $("<input type='hidden'/>").attr("name", validator.submitButton.name).val(validator.submitButton.value).appendTo(validator.currentForm);
						}
						validator.settings.submitHandler.call( validator, validator.currentForm );
						if (validator.submitButton) {
							// and clean up afterwards; thanks to no-block-scope, hidden can be referenced
							hidden.remove();
						}
						return false;
					}
					return true;
				}
					
				// prevent submit for invalid forms or custom submit handlers
				if ( validator.cancelSubmit ) {
					validator.cancelSubmit = false;
					return handle();
				}
				if ( validator.form() ) {
					if ( validator.pendingRequest ) {
						validator.formSubmitted = true;
						return false;
					}
					return handle();
				} else {
					validator.focusInvalid();
					return false;
				}
			});
		}
		
		return validator;
	},
	// http://docs.jquery.com/Plugins/Validation/valid
	valid: function() {
        if ( $(this[0]).is('form')) {
            return this.validate().form();
        } else {
            var valid = true;
            var validator = $(this[0].form).validate();
            this.each(function() {
				valid &= validator.element(this);
            });
            return valid;
        }
    },
	// attributes: space seperated list of attributes to retrieve and remove
	removeAttrs: function(attributes) {
		var result = {},
			$element = this;
		$.each(attributes.split(/\s/), function(index, value) {
			result[value] = $element.attr(value);
			$element.removeAttr(value);
		});
		return result;
	},
	// http://docs.jquery.com/Plugins/Validation/rules
	rules: function(command, argument) {
		var element = this[0];
		
		if (command) {
			var settings = $.data(element.form, 'validator').settings;
			var staticRules = settings.rules;
			var existingRules = $.validator.staticRules(element);
			switch(command) {
			case "add":
				$.extend(existingRules, $.validator.normalizeRule(argument));
				staticRules[element.name] = existingRules;
				if (argument.messages)
					settings.messages[element.name] = $.extend( settings.messages[element.name], argument.messages );
				break;
			case "remove":
				if (!argument) {
					delete staticRules[element.name];
					return existingRules;
				}
				var filtered = {};
				$.each(argument.split(/\s/), function(index, method) {
					filtered[method] = existingRules[method];
					delete existingRules[method];
				});
				return filtered;
			}
		}
		
		var data = $.validator.normalizeRules(
		$.extend(
			{},
			$.validator.metadataRules(element),
			$.validator.classRules(element),
			$.validator.attributeRules(element),
			$.validator.staticRules(element)
		), element);
		
		// make sure required is at front
		if (data.required) {
			var param = data.required;
			delete data.required;
			data = $.extend({required: param}, data);
		}
		
		return data;
	}
});

// Custom selectors
$.extend($.expr[":"], {
	// http://docs.jquery.com/Plugins/Validation/blank
	blank: function(a) {return !$.trim("" + a.value);},
	// http://docs.jquery.com/Plugins/Validation/filled
	filled: function(a) {return !!$.trim("" + a.value);},
	// http://docs.jquery.com/Plugins/Validation/unchecked
	unchecked: function(a) {return !a.checked;}
});

// constructor for validator
$.validator = function( options, form ) {
	this.settings = $.extend( {}, $.validator.defaults, options );
	this.currentForm = form;
	this.init();
};

$.validator.format = function(source, params) {
	if ( arguments.length == 1 ) 
		return function() {
			var args = $.makeArray(arguments);
			args.unshift(source);
			return $.validator.format.apply( this, args );
		};
	if ( arguments.length > 2 && params.constructor != Array  ) {
		params = $.makeArray(arguments).slice(1);
	}
	if ( params.constructor != Array ) {
		params = [ params ];
	}
	$.each(params, function(i, n) {
		source = source.replace(new RegExp("\\{" + i + "\\}", "g"), n);
	});
	return source;
};

$.extend($.validator, {
	
	defaults: {
		messages: {},
		groups: {},
		rules: {},
		errorClass: "error",
		validClass: "valid",
		errorElement: "label",
		focusInvalid: true,
		errorContainer: $( [] ),
		errorLabelContainer: $( [] ),
		onsubmit: true,
		ignore: [],
		ignoreTitle: false,
		onfocusin: function(element) {
			this.lastActive = element;
				
			// hide error label and remove error class on focus if enabled
			if ( this.settings.focusCleanup && !this.blockFocusCleanup ) {
				this.settings.unhighlight && this.settings.unhighlight.call( this, element, this.settings.errorClass, this.settings.validClass );
				this.errorsFor(element).hide();
			}
		},
		onfocusout: function(element) {
			if ( !this.checkable(element) && (element.name in this.submitted || !this.optional(element)) ) {
				this.element(element);
			}
		},
		onkeyup: function(element) {
			if ( element.name in this.submitted || element == this.lastElement ) {
				this.element(element);
			}
		},
		onclick: function(element) {
			// click on selects, radiobuttons and checkboxes
			if ( element.name in this.submitted )
				this.element(element);
			// or option elements, check parent select in that case
			else if (element.parentNode.name in this.submitted)
				this.element(element.parentNode)
		},
		highlight: function( element, errorClass, validClass ) {
			$(element).addClass(errorClass).removeClass(validClass);
		},
		unhighlight: function( element, errorClass, validClass ) {
			$(element).removeClass(errorClass).addClass(validClass);
		}
	},

	// http://docs.jquery.com/Plugins/Validation/Validator/setDefaults
	setDefaults: function(settings) {
		$.extend( $.validator.defaults, settings );
	},

	messages: {
		required: "This field is required.",
		remote: "Please fix this field.",
		email: "Please enter a valid email address.",
		url: "Please enter a valid URL.",
		date: "Please enter a valid date.",
		dateISO: "Please enter a valid date (ISO).",
		number: "Please enter a valid number.",
		digits: "Please enter only digits.",
		creditcard: "Please enter a valid credit card number.",
		equalTo: "Please enter the same value again.",
		accept: "Please enter a value with a valid extension.",
		maxlength: $.validator.format("Please enter no more than {0} characters."),
		minlength: $.validator.format("Please enter at least {0} characters."),
		rangelength: $.validator.format("Please enter a value between {0} and {1} characters long."),
		range: $.validator.format("Please enter a value between {0} and {1}."),
		max: $.validator.format("Please enter a value less than or equal to {0}."),
		min: $.validator.format("Please enter a value greater than or equal to {0}.")
	},
	
	autoCreateRanges: false,
	
	prototype: {
		
		init: function() {
			this.labelContainer = $(this.settings.errorLabelContainer);
			this.errorContext = this.labelContainer.length && this.labelContainer || $(this.currentForm);
			this.containers = $(this.settings.errorContainer).add( this.settings.errorLabelContainer );
			this.submitted = {};
			this.valueCache = {};
			this.pendingRequest = 0;
			this.pending = {};
			this.invalid = {};
			this.reset();
			
			var groups = (this.groups = {});
			$.each(this.settings.groups, function(key, value) {
				$.each(value.split(/\s/), function(index, name) {
					groups[name] = key;
				});
			});
			var rules = this.settings.rules;
			$.each(rules, function(key, value) {
				rules[key] = $.validator.normalizeRule(value);
			});
			
			function delegate(event) {
				var validator = $.data(this[0].form, "validator");
				validator.settings["on" + event.type] && validator.settings["on" + event.type].call(validator, this[0] );
			}
			$(this.currentForm)
				.delegate("focusin focusout keyup", ":text, :password, :file, select, textarea", delegate)
				.delegate("click", ":radio, :checkbox, select, option", delegate);

			if (this.settings.invalidHandler)
				$(this.currentForm).bind("invalid-form.validate", this.settings.invalidHandler);
		},

		// http://docs.jquery.com/Plugins/Validation/Validator/form
		form: function() {
			this.checkForm();
			$.extend(this.submitted, this.errorMap);
			this.invalid = $.extend({}, this.errorMap);
			if (!this.valid())
				$(this.currentForm).triggerHandler("invalid-form", [this]);
			this.showErrors();
			return this.valid();
		},
		
		checkForm: function() {
			this.prepareForm();
			for ( var i = 0, elements = (this.currentElements = this.elements()); elements[i]; i++ ) {
				this.check( elements[i] );
			}
			return this.valid(); 
		},
		
		// http://docs.jquery.com/Plugins/Validation/Validator/element
		element: function( element ) {
			element = this.clean( element );
			this.lastElement = element;
			this.prepareElement( element );
			this.currentElements = $(element);
			var result = this.check( element );
			if ( result ) {
				delete this.invalid[element.name];
			} else {
				this.invalid[element.name] = true;
			}
			if ( !this.numberOfInvalids() ) {
				// Hide error containers on last error
				this.toHide = this.toHide.add( this.containers );
			}
			this.showErrors();
			return result;
		},

		// http://docs.jquery.com/Plugins/Validation/Validator/showErrors
		showErrors: function(errors) {
			if(errors) {
				// add items to error list and map
				$.extend( this.errorMap, errors );
				this.errorList = [];
				for ( var name in errors ) {
					this.errorList.push({
						message: errors[name],
						element: this.findByName(name)[0]
					});
				}
				// remove items from success list
				this.successList = $.grep( this.successList, function(element) {
					return !(element.name in errors);
				});
			}
			this.settings.showErrors
				? this.settings.showErrors.call( this, this.errorMap, this.errorList )
				: this.defaultShowErrors();
		},
		
		// http://docs.jquery.com/Plugins/Validation/Validator/resetForm
		resetForm: function() {
			if ( $.fn.resetForm )
				$( this.currentForm ).resetForm();
			this.submitted = {};
			this.prepareForm();
			this.hideErrors();
			this.elements().removeClass( this.settings.errorClass );
		},
		
		numberOfInvalids: function() {
			return this.objectLength(this.invalid);
		},
		
		objectLength: function( obj ) {
			var count = 0;
			for ( var i in obj )
				count++;
			return count;
		},
		
		hideErrors: function() {
			this.addWrapper( this.toHide ).hide();
		},
		
		valid: function() {
			return this.size() == 0;
		},
		
		size: function() {
			return this.errorList.length;
		},
		
		focusInvalid: function() {
			if( this.settings.focusInvalid ) {
				try {
					$(this.findLastActive() || this.errorList.length && this.errorList[0].element || []).filter(":visible").focus();
				} catch(e) {
					// ignore IE throwing errors when focusing hidden elements
				}
			}
		},
		
		findLastActive: function() {
			var lastActive = this.lastActive;
			return lastActive && $.grep(this.errorList, function(n) {
				return n.element.name == lastActive.name;
			}).length == 1 && lastActive;
		},
		
		elements: function() {
			var validator = this,
				rulesCache = {};
			
			// select all valid inputs inside the form (no submit or reset buttons)
			// workaround $Query([]).add until http://dev.jquery.com/ticket/2114 is solved
			return $([]).add(this.currentForm.elements)
			.filter(":input")
			.not(":submit, :reset, :image, [disabled]")
			.not( this.settings.ignore )
			.filter(function() {
				!this.name && validator.settings.debug && window.console && console.error( "%o has no name assigned", this);
			
				// select only the first element for each name, and only those with rules specified
				if ( this.name in rulesCache || !validator.objectLength($(this).rules()) )
					return false;
				
				rulesCache[this.name] = true;
				return true;
			});
		},
		
		clean: function( selector ) {
			return $( selector )[0];
		},
		
		errors: function() {
			return $( this.settings.errorElement + "." + this.settings.errorClass, this.errorContext );
		},
		
		reset: function() {
			this.successList = [];
			this.errorList = [];
			this.errorMap = {};
			this.toShow = $([]);
			this.toHide = $([]);
			this.currentElements = $([]);
		},
		
		prepareForm: function() {
			this.reset();
			this.toHide = this.errors().add( this.containers );
		},
		
		prepareElement: function( element ) {
			this.reset();
			this.toHide = this.errorsFor(element);
		},
	
		check: function( element ) {
			element = this.clean( element );
			
			// if radio/checkbox, validate first element in group instead
			if (this.checkable(element)) {
				element = this.findByName( element.name )[0];
			}
			
			var rules = $(element).rules();
			var dependencyMismatch = false;
			for( method in rules ) {
				var rule = { method: method, parameters: rules[method] };
				try {
					var result = $.validator.methods[method].call( this, element.value.replace(/\r/g, ""), element, rule.parameters );
					
					// if a method indicates that the field is optional and therefore valid,
					// don't mark it as valid when there are no other rules
					if ( result == "dependency-mismatch" ) {
						dependencyMismatch = true;
						continue;
					}
					dependencyMismatch = false;
					
					if ( result == "pending" ) {
						this.toHide = this.toHide.not( this.errorsFor(element) );
						return;
					}
					
					if( !result ) {
						this.formatAndAdd( element, rule );
						return false;
					}
				} catch(e) {
					this.settings.debug && window.console && console.log("exception occured when checking element " + element.id
						 + ", check the '" + rule.method + "' method", e);
					throw e;
				}
			}
			if (dependencyMismatch)
				return;
			if ( this.objectLength(rules) )
				this.successList.push(element);
			return true;
		},
		
		// return the custom message for the given element and validation method
		// specified in the element's "messages" metadata
		customMetaMessage: function(element, method) {
			if (!$.metadata)
				return;
			
			var meta = this.settings.meta
				? $(element).metadata()[this.settings.meta]
				: $(element).metadata();
			
			return meta && meta.messages && meta.messages[method];
		},
		
		// return the custom message for the given element name and validation method
		customMessage: function( name, method ) {
			var m = this.settings.messages[name];
			return m && (m.constructor == String
				? m
				: m[method]);
		},
		
		// return the first defined argument, allowing empty strings
		findDefined: function() {
			for(var i = 0; i < arguments.length; i++) {
				if (arguments[i] !== undefined)
					return arguments[i];
			}
			return undefined;
		},
		
		defaultMessage: function( element, method) {
			return this.findDefined(
				this.customMessage( element.name, method ),
				this.customMetaMessage( element, method ),
				// title is never undefined, so handle empty string as undefined
				!this.settings.ignoreTitle && element.title || undefined,
				$.validator.messages[method],
				"<strong>Warning: No message defined for " + element.name + "</strong>"
			);
		},
		
		formatAndAdd: function( element, rule ) {
			var message = this.defaultMessage( element, rule.method ),
				theregex = /\$?\{(\d+)\}/g;
			if ( typeof message == "function" ) {
				message = message.call(this, rule.parameters, element);
			} else if (theregex.test(message)) {
				message = jQuery.format(message.replace(theregex, '{$1}'), rule.parameters);
			}			
			this.errorList.push({
				message: message,
				element: element
			});
			
			this.errorMap[element.name] = message;
			this.submitted[element.name] = message;
		},
		
		addWrapper: function(toToggle) {
			if ( this.settings.wrapper )
				toToggle = toToggle.add( toToggle.parent( this.settings.wrapper ) );
			return toToggle;
		},
		
		defaultShowErrors: function() {
			for ( var i = 0; this.errorList[i]; i++ ) {
				var error = this.errorList[i];
				this.settings.highlight && this.settings.highlight.call( this, error.element, this.settings.errorClass, this.settings.validClass );
				this.showLabel( error.element, error.message );
			}
			if( this.errorList.length ) {
				this.toShow = this.toShow.add( this.containers );
			}
			if (this.settings.success) {
				for ( var i = 0; this.successList[i]; i++ ) {
					this.showLabel( this.successList[i] );
				}
			}
			if (this.settings.unhighlight) {
				for ( var i = 0, elements = this.validElements(); elements[i]; i++ ) {
					this.settings.unhighlight.call( this, elements[i], this.settings.errorClass, this.settings.validClass );
				}
			}
			this.toHide = this.toHide.not( this.toShow );
			this.hideErrors();
			this.addWrapper( this.toShow ).show();
		},
		
		validElements: function() {
			return this.currentElements.not(this.invalidElements());
		},
		
		invalidElements: function() {
			return $(this.errorList).map(function() {
				return this.element;
			});
		},
		
		showLabel: function(element, message) {
			var label = this.errorsFor( element );
			if ( label.length ) {
				// refresh error/success class
				label.removeClass().addClass( this.settings.errorClass );
			
				// check if we have a generated label, replace the message then
				label.attr("generated") && label.html(message);
			} else {
				// create label
				label = $("<" + this.settings.errorElement + "/>")
					.attr({"for":  this.idOrName(element), generated: true})
					.addClass(this.settings.errorClass)
					.html(message || "");
				if ( this.settings.wrapper ) {
					// make sure the element is visible, even in IE
					// actually showing the wrapped element is handled elsewhere
					label = label.hide().show().wrap("<" + this.settings.wrapper + "/>").parent();
				}
				if ( !this.labelContainer.append(label).length )
					this.settings.errorPlacement
						? this.settings.errorPlacement(label, $(element) )
						: label.insertAfter(element);
			}
			if ( !message && this.settings.success ) {
				label.text("");
				typeof this.settings.success == "string"
					? label.addClass( this.settings.success )
					: this.settings.success( label );
			}
			this.toShow = this.toShow.add(label);
		},
		
		errorsFor: function(element) {
			var name = this.idOrName(element);
    		return this.errors().filter(function() {
				return $(this).attr('for') == name
			});
		},
		
		idOrName: function(element) {
			return this.groups[element.name] || (this.checkable(element) ? element.name : element.id || element.name);
		},

		checkable: function( element ) {
			return /radio|checkbox/i.test(element.type);
		},
		
		findByName: function( name ) {
			// select by name and filter by form for performance over form.find("[name=...]")
			var form = this.currentForm;
			return $(document.getElementsByName(name)).map(function(index, element) {
				return element.form == form && element.name == name && element  || null;
			});
		},
		
		getLength: function(value, element) {
			switch( element.nodeName.toLowerCase() ) {
			case 'select':
				return $("option:selected", element).length;
			case 'input':
				if( this.checkable( element) )
					return this.findByName(element.name).filter(':checked').length;
			}
			return value.length;
		},
	
		depend: function(param, element) {
			return this.dependTypes[typeof param]
				? this.dependTypes[typeof param](param, element)
				: true;
		},
	
		dependTypes: {
			"boolean": function(param, element) {
				return param;
			},
			"string": function(param, element) {
				return !!$(param, element.form).length;
			},
			"function": function(param, element) {
				return param(element);
			}
		},
		
		optional: function(element) {
			return !$.validator.methods.required.call(this, $.trim(element.value), element) && "dependency-mismatch";
		},
		
		startRequest: function(element) {
			if (!this.pending[element.name]) {
				this.pendingRequest++;
				this.pending[element.name] = true;
			}
		},
		
		stopRequest: function(element, valid) {
			this.pendingRequest--;
			// sometimes synchronization fails, make sure pendingRequest is never < 0
			if (this.pendingRequest < 0)
				this.pendingRequest = 0;
			delete this.pending[element.name];
			if ( valid && this.pendingRequest == 0 && this.formSubmitted && this.form() ) {
				$(this.currentForm).submit();
				this.formSubmitted = false;
			} else if (!valid && this.pendingRequest == 0 && this.formSubmitted) {
				$(this.currentForm).triggerHandler("invalid-form", [this]);
				this.formSubmitted = false;
			}
		},
		
		previousValue: function(element) {
			return $.data(element, "previousValue") || $.data(element, "previousValue", {
				old: null,
				valid: true,
				message: this.defaultMessage( element, "remote" )
			});
		}
		
	},
	
	classRuleSettings: {
		required: {required: true},
		email: {email: true},
		url: {url: true},
		date: {date: true},
		dateISO: {dateISO: true},
		dateDE: {dateDE: true},
		number: {number: true},
		numberDE: {numberDE: true},
		digits: {digits: true},
		creditcard: {creditcard: true}
	},
	
	addClassRules: function(className, rules) {
		className.constructor == String ?
			this.classRuleSettings[className] = rules :
			$.extend(this.classRuleSettings, className);
	},
	
	classRules: function(element) {
		var rules = {};
		var classes = $(element).attr('class');
		classes && $.each(classes.split(' '), function() {
			if (this in $.validator.classRuleSettings) {
				$.extend(rules, $.validator.classRuleSettings[this]);
			}
		});
		return rules;
	},
	
	attributeRules: function(element) {
		var rules = {};
		var $element = $(element);
		
		for (method in $.validator.methods) {
			var value = $element.attr(method);
			if (value) {
				rules[method] = value;
			}
		}
		
		// maxlength may be returned as -1, 2147483647 (IE) and 524288 (safari) for text inputs
		if (rules.maxlength && /-1|2147483647|524288/.test(rules.maxlength)) {
			delete rules.maxlength;
		}
		
		return rules;
	},
	
	metadataRules: function(element) {
		if (!$.metadata) return {};
		
		var meta = $.data(element.form, 'validator').settings.meta;
		return meta ?
			$(element).metadata()[meta] :
			$(element).metadata();
	},
	
	staticRules: function(element) {
		var rules = {};
		var validator = $.data(element.form, 'validator');
		if (validator.settings.rules) {
			rules = $.validator.normalizeRule(validator.settings.rules[element.name]) || {};
		}
		return rules;
	},
	
	normalizeRules: function(rules, element) {
		// handle dependency check
		$.each(rules, function(prop, val) {
			// ignore rule when param is explicitly false, eg. required:false
			if (val === false) {
				delete rules[prop];
				return;
			}
			if (val.param || val.depends) {
				var keepRule = true;
				switch (typeof val.depends) {
					case "string":
						keepRule = !!$(val.depends, element.form).length;
						break;
					case "function":
						keepRule = val.depends.call(element, element);
						break;
				}
				if (keepRule) {
					rules[prop] = val.param !== undefined ? val.param : true;
				} else {
					delete rules[prop];
				}
			}
		});
		
		// evaluate parameters
		$.each(rules, function(rule, parameter) {
			rules[rule] = $.isFunction(parameter) ? parameter(element) : parameter;
		});
		
		// clean number parameters
		$.each(['minlength', 'maxlength', 'min', 'max'], function() {
			if (rules[this]) {
				rules[this] = Number(rules[this]);
			}
		});
		$.each(['rangelength', 'range'], function() {
			if (rules[this]) {
				rules[this] = [Number(rules[this][0]), Number(rules[this][1])];
			}
		});
		
		if ($.validator.autoCreateRanges) {
			// auto-create ranges
			if (rules.min && rules.max) {
				rules.range = [rules.min, rules.max];
				delete rules.min;
				delete rules.max;
			}
			if (rules.minlength && rules.maxlength) {
				rules.rangelength = [rules.minlength, rules.maxlength];
				delete rules.minlength;
				delete rules.maxlength;
			}
		}
		
		// To support custom messages in metadata ignore rule methods titled "messages"
		if (rules.messages) {
			delete rules.messages
		}
		
		return rules;
	},
	
	// Converts a simple string to a {string: true} rule, e.g., "required" to {required:true}
	normalizeRule: function(data) {
		if( typeof data == "string" ) {
			var transformed = {};
			$.each(data.split(/\s/), function() {
				transformed[this] = true;
			});
			data = transformed;
		}
		return data;
	},
	
	// http://docs.jquery.com/Plugins/Validation/Validator/addMethod
	addMethod: function(name, method, message) {
		$.validator.methods[name] = method;
		$.validator.messages[name] = message != undefined ? message : $.validator.messages[name];
		if (method.length < 3) {
			$.validator.addClassRules(name, $.validator.normalizeRule(name));
		}
	},

	methods: {

		// http://docs.jquery.com/Plugins/Validation/Methods/required
		required: function(value, element, param) {
			// check if dependency is met
			if ( !this.depend(param, element) )
				return "dependency-mismatch";
			switch( element.nodeName.toLowerCase() ) {
			case 'select':
				// could be an array for select-multiple or a string, both are fine this way
				var val = $(element).val();
				return val && val.length > 0;
			case 'input':
				if ( this.checkable(element) )
					return this.getLength(value, element) > 0;
			default:
				return $.trim(value).length > 0;
			}
		},
		
		// http://docs.jquery.com/Plugins/Validation/Methods/remote
		remote: function(value, element, param) {
			if ( this.optional(element) )
				return "dependency-mismatch";
			
			var previous = this.previousValue(element);
			if (!this.settings.messages[element.name] )
				this.settings.messages[element.name] = {};
			previous.originalMessage = this.settings.messages[element.name].remote;
			this.settings.messages[element.name].remote = previous.message;
			
			param = typeof param == "string" && {url:param} || param; 
			
			if ( previous.old !== value ) {
				previous.old = value;
				var validator = this;
				this.startRequest(element);
				var data = {};
				data[element.name] = value;
				$.ajax($.extend(true, {
					url: param,
					mode: "abort",
					port: "validate" + element.name,
					dataType: "json",
					data: data,
					success: function(response) {
						validator.settings.messages[element.name].remote = previous.originalMessage;
						var valid = response === true;
						if ( valid ) {
							var submitted = validator.formSubmitted;
							validator.prepareElement(element);
							validator.formSubmitted = submitted;
							validator.successList.push(element);
							validator.showErrors();
						} else {
							var errors = {};
							var message = (previous.message = response || validator.defaultMessage( element, "remote" ));
							errors[element.name] = $.isFunction(message) ? message(value) : message;
							validator.showErrors(errors);
						}
						previous.valid = valid;
						validator.stopRequest(element, valid);
					}
				}, param));
				return "pending";
			} else if( this.pending[element.name] ) {
				return "pending";
			}
			return previous.valid;
		},

		// http://docs.jquery.com/Plugins/Validation/Methods/minlength
		minlength: function(value, element, param) {
			return this.optional(element) || this.getLength($.trim(value), element) >= param;
		},
		
		// http://docs.jquery.com/Plugins/Validation/Methods/maxlength
		maxlength: function(value, element, param) {
			return this.optional(element) || this.getLength($.trim(value), element) <= param;
		},
		
		// http://docs.jquery.com/Plugins/Validation/Methods/rangelength
		rangelength: function(value, element, param) {
			var length = this.getLength($.trim(value), element);
			return this.optional(element) || ( length >= param[0] && length <= param[1] );
		},
		
		// http://docs.jquery.com/Plugins/Validation/Methods/min
		min: function( value, element, param ) {
			return this.optional(element) || value >= param;
		},
		
		// http://docs.jquery.com/Plugins/Validation/Methods/max
		max: function( value, element, param ) {
			return this.optional(element) || value <= param;
		},
		
		// http://docs.jquery.com/Plugins/Validation/Methods/range
		range: function( value, element, param ) {
			return this.optional(element) || ( value >= param[0] && value <= param[1] );
		},
		
		// http://docs.jquery.com/Plugins/Validation/Methods/email
		email: function(value, element) {
			// contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
			return this.optional(element) || /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i.test(value);
		},
	
		// http://docs.jquery.com/Plugins/Validation/Methods/url
		url: function(value, element) {
			// contributed by Scott Gonzalez: http://projects.scottsplayground.com/iri/
			return this.optional(element) || /^(https?|ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(value);
		},
        
		// http://docs.jquery.com/Plugins/Validation/Methods/date
		date: function(value, element) {
			return this.optional(element) || !/Invalid|NaN/.test(new Date(value));
		},
	
		// http://docs.jquery.com/Plugins/Validation/Methods/dateISO
		dateISO: function(value, element) {
			return this.optional(element) || /^\d{4}[\/-]\d{1,2}[\/-]\d{1,2}$/.test(value);
		},
	
		// http://docs.jquery.com/Plugins/Validation/Methods/number
		number: function(value, element) {
			return this.optional(element) || /^-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?$/.test(value);
		},
	
		// http://docs.jquery.com/Plugins/Validation/Methods/digits
		digits: function(value, element) {
			return this.optional(element) || /^\d+$/.test(value);
		},
		
		// http://docs.jquery.com/Plugins/Validation/Methods/creditcard
		// based on http://en.wikipedia.org/wiki/Luhn
		creditcard: function(value, element) {
			if ( this.optional(element) )
				return "dependency-mismatch";
			// accept only digits and dashes
			if (/[^0-9-]+/.test(value))
				return false;
			var nCheck = 0,
				nDigit = 0,
				bEven = false;

			value = value.replace(/\D/g, "");

			for (var n = value.length - 1; n >= 0; n--) {
				var cDigit = value.charAt(n);
				var nDigit = parseInt(cDigit, 10);
				if (bEven) {
					if ((nDigit *= 2) > 9)
						nDigit -= 9;
				}
				nCheck += nDigit;
				bEven = !bEven;
			}

			return (nCheck % 10) == 0;
		},
		
		// http://docs.jquery.com/Plugins/Validation/Methods/accept
		accept: function(value, element, param) {
			param = typeof param == "string" ? param.replace(/,/g, '|') : "png|jpe?g|gif";
			return this.optional(element) || value.match(new RegExp(".(" + param + ")$", "i")); 
		},
		
		// http://docs.jquery.com/Plugins/Validation/Methods/equalTo
		equalTo: function(value, element, param) {
			// bind to the blur event of the target in order to revalidate whenever the target field is updated
			// TODO find a way to bind the event just once, avoiding the unbind-rebind overhead
			var target = $(param).unbind(".validate-equalTo").bind("blur.validate-equalTo", function() {
				$(element).valid();
			});
			return value == target.val();
		}
		
	}
	
});

// deprecated, use $.validator.format instead
$.format = $.validator.format;

})(jQuery);

// ajax mode: abort
// usage: $.ajax({ mode: "abort"[, port: "uniqueport"]});
// if mode:"abort" is used, the previous request on that port (port can be undefined) is aborted via XMLHttpRequest.abort() 
;(function($) {
	var ajax = $.ajax;
	var pendingRequests = {};
	$.ajax = function(settings) {
		// create settings for compatibility with ajaxSetup
		settings = $.extend(settings, $.extend({}, $.ajaxSettings, settings));
		var port = settings.port;
		if (settings.mode == "abort") {
			if ( pendingRequests[port] ) {
				pendingRequests[port].abort();
			}
			return (pendingRequests[port] = ajax.apply(this, arguments));
		}
		return ajax.apply(this, arguments);
	};
})(jQuery);

// provides cross-browser focusin and focusout events
// IE has native support, in other browsers, use event caputuring (neither bubbles)

// provides delegate(type: String, delegate: Selector, handler: Callback) plugin for easier event delegation
// handler is only called when $(event.target).is(delegate), in the scope of the jquery-object for event.target 

// provides triggerEvent(type: String, target: Element) to trigger delegated events
;(function($) {
	$.each({
		focus: 'focusin',
		blur: 'focusout'	
	}, function( original, fix ){
		$.event.special[fix] = {
			setup:function() {
				if ( $.browser.msie ) return false;
				this.addEventListener( original, $.event.special[fix].handler, true );
			},
			teardown:function() {
				if ( $.browser.msie ) return false;
				this.removeEventListener( original,
				$.event.special[fix].handler, true );
			},
			handler: function(e) {
				arguments[0] = $.event.fix(e);
				arguments[0].type = fix;
				return $.event.handle.apply(this, arguments);
			}
		};
	});
	$.extend($.fn, {
		delegate: function(type, delegate, handler) {
			return this.bind(type, function(event) {
				var target = $(event.target);
				if (target.is(delegate)) {
					return handler.apply(target, arguments);
				}
			});
		},
		triggerEvent: function(type, target) {
			return this.triggerHandler(type, [$.event.fix({ type: type, target: target })]);
		}
	})
})(jQuery);

function URLify(s, num_chars) {
    // changes, e.g., "Petty theft" to "petty_theft"
    // remove all these words from the string before urlifying
    removelist = ["a", "an", "as", "at", "before", "but", "by", "for", "from",
                  "is", "in", "into", "like", "of", "off", "on", "onto", "per",
                  "since", "than", "the", "this", "that", "to", "up", "via",
                  "with"];
    r = new RegExp('\\b(' + removelist.join('|') + ')\\b', 'gi');
    s = s.replace(r, '');
    // if downcode doesn't hit, the char will be stripped here
    s = s.replace(/[^-\w\s]/g, '');  // remove unneeded chars
    s = s.replace(/^\s+|\s+$/g, ''); // trim leading/trailing spaces
    s = s.replace(/[-\s]+/g, '-');   // convert spaces to hyphens
    s = s.toLowerCase();             // convert to lowercase
    return s.substring(0, num_chars);// trim to first num_chars chars
}

