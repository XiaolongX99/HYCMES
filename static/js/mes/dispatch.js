//dispatch.jquery-2.0.3,2018-06-01

$(document).ready(function(){	

		var rows=0;  //行号
		HTMLStart();

		//自动派工
		$("#dispatch").click(function(){
		    var dep = $("#dispatchdep").val();
		    var cell = $("#dispatchcell").val();
		    var operation = $("#dispatchoperation").val();
		    var po = $("#dispatchpo").val();
		    var poid = $("#dispatchpoid").val();
		    var wo = $("#dispatchwo").val();
		    var item = $("#item").val();
		    var trid = $("#triduuid").text();
		    var dg1 = $("#daterange1").val();
		    var dg2 = $("#daterange2").val();
		    var lotsize = $("#lotsize").val();
		    var lotqty = $("#lotqty").val();
		    var dispatchqty = $("#dispatchqty").val();    
		    var sntype = $("#sntype").prop('checked');
		    var boms=JSON.stringify(bomjson());
		    var sns=JSON.stringify(snjson());
		    var routs=JSON.stringify(routjson());

				$.ajax({
					url:"/sfm/dispatch/dispatch/",
					type:"POST",
					data:{'dep':dep,'cell':cell,'operation':operation,'po':po,'poid':poid,'wo':wo,'item':item,'trid':trid,'dg1':dg1,'dg2':dg2,'lotsize':lotsize,'lotqty':lotqty,'dispatchqty':dispatchqty,'sntype':sntype,'boms':boms,'sns':sns,'routs':routs},
					dataType:"json",
					success:function(ret){
						$("#dispatchqty").val(0);
						$("#lotqty").val(0); 
				        $('#triduuid').empty();
	        			$('#triduuid').append(uuid());  

						if (sntype==true){	
							snlist(ret);
							alert('完成派工:'+ dispatchqty);
						}else{
							$('#SNID').find("tr").not(':eq(0)').remove();
							alert('完成派单:'+ dispatchqty);
						};
					},
				});		
			});

		//打印流程单
		$("#printsn").click(function(){
		    var cell = $("#dispatchcell").val();
		    var po = $("#dispatchpo").val();		    
		    var wo = $("#dispatchwo").val();
		    var item = $("#item").val();		    
		    var sns=JSON.stringify(snjson());

		    //$.each(sns,function(i,item){	
				$.ajax({
					url:"/sfm/dispatch/printsn/",
					type:"POST",
					data:{'cell':cell,'po':po,'wo':wo,'item':item,'sns':sns},
					dataType:"json",
					success:function(ret){
						snprint(ret);
						//return false;
						},
					});	



				//});
				return false;
			});

			
		$("#dispatchdep").change(function(){
	        $('#triduuid').empty();
	        $('#triduuid').append(uuid());
	        $('#dispatchpoid').empty();
	        $('#dispatchwo').empty();
	        var dep = $("#dispatchdep").val();
			$.ajax({
					url:"/sfm/dispatch/dep/",
					type:"POST",
					data:{'dep':dep,'sle':'1'},
					dataType:"json",
					success:function(ret){	
						cells(ret);
						//operations(ret);
						var cell=$("#dispatchcell").val();					
						$.ajax({
								url:"/sfm/dispatch/cell/",
								type:"POST",
								data:{'cell':cell,'sle':'1'},
								dataType:"json",
								success:function(ret){	
									operations(ret);
								},
						});							
					},
				});		
			});


		$("#dispatchcell").change(function(){
	        $('#triduuid').empty();
	        $('#triduuid').append(uuid());
	        var cell = $("#dispatchcell").val();
			$.ajax({
					url:"/sfm/dispatch/cell/",
					type:"POST",
					data:{'cell':cell,'sle':'1'},
					dataType:"json",
					success:function(ret){	
						operations(ret);	
					},
				});		
			});


	    $('#dispatchpo').on('blur',function(event){    
			$('#triduuid').empty();
			$('#triduuid').append(uuid());
		    var dep = $("#dispatchdep").val();
		    var cell = $("#dispatchcell").val();
		    var operation = $("#ERPoperation").val();
		    var po = $("#dispatchpo").val();
		    var wostate = $("#wostates").prop('checked');
		    //alert(event.keyCode );
	        //if(event.keyCode == "13"){   
					$.ajax({
						url:"/sfm/dispatch/po/",
						type:"POST",
						data:{'dep':dep,'cell':cell,'operation':operation,'po':po,'sle':wostate},
						dataType:"json",
						success:function(ret){	
							poids(ret);
						    var poid = $("#dispatchpoid").val();
							$.ajax({
									url:"/sfm/dispatch/poid/",
									type:"POST",
									data:{'dep':dep,'cell':cell,'operation':operation,'po':po,'poid':poid,'sle':wostate},
									dataType:"json",
									success:function(ret){	
										wos(ret);
										var wo = $("#dispatchwo").val();
										$.ajax({
												url:"/sfm/dispatch/wo/",
												type:"POST",
												data:{'dep':dep,'wo':wo,'sle':wostate},
												dataType:"json",
												success:function(ret){	
													woinfos(ret);
													boms(ret);
													snlist(ret);
													var item = $("#item").val(); 
													$.ajax({
														url:"/sfm/dispatch/item/",
														type:"POST",
														data:{'dep':dep,'item':item},
														dataType:"json",
														success:function(ret){	
															$("#item").attr("disabled",true); 
															parameters(ret);
															routings(ret);
														},
													});	
												},
											});	
									},
								});
							},
						});	
					return false;  
	            //}  
	        });


	    $('#dispatchpoid').change(function(){  
			$('#triduuid').empty();
			$('#triduuid').append(uuid());			
		    var dep = $("#dispatchdep").val();
		    var cell = $("#dispatchcell").val();
		    var operation = $("#ERPoperation").val();
		    var po = $("#dispatchpo").val();
		    var poid = $("#dispatchpoid").val();
		    var wostate = $("#wostates").prop('checked');

			$.ajax({
					url:"/sfm/dispatch/poid/",
					type:"POST",
					data:{'dep':dep,'cell':cell,'operation':operation,'po':po,'poid':poid,'sle':wostate},
					dataType:"json",
					success:function(ret){	
						wos(ret);
						var wo2 = $("#dispatchwo").val();
						$.ajax({
							url:"/sfm/dispatch/wo/",
							type:"POST",
							data:{'dep':dep,'wo':wo2,'sle':wostate},
							dataType:"json",
							success:function(ret){	
								woinfos(ret);
								boms(ret);	
								snlist(ret);
								var item3 = $("#item").val(); 
								$.ajax({
									url:"/sfm/dispatch/item/",
									type:"POST",
									data:{'dep':dep,'item':item3},
									dataType:"json",
									success:function(ret){	
										parameters(ret);
										routings(ret);
									},
								});	
							},
						});		
					},
				});		
			});
 

	    $('#dispatchwo').change(function(){  
			$('#triduuid').empty();
			$('#triduuid').append(uuid());
		    var dep = $("#dispatchdep").val();
			var wo = $("#dispatchwo").val();
		    var wostate = $("#wostates").prop('checked');			

			$.ajax({
					url:"/sfm/dispatch/wo/",
					type:"POST",
					data:{'dep':dep,'wo':wo,'sle':wostate},
					dataType:"json",
					success:function(ret){	
						woinfos(ret);
						boms(ret);
						snlist(ret);
						var item2 = $("#item").val(); 
						$.ajax({
							url:"/sfm/dispatch/item/",
							type:"POST",
							data:{'dep':dep,'item':item2},
							dataType:"json",
							success:function(ret){	
								parameters(ret);
								routings(ret);
							},
						});	
					},
				});		
			});


	    $('#item').on('keypress',function(event){ 
	    	$('#item').cbNum();
	    	var dep = $("#dispatchdep").val();
	    	var item = $("#item").val(); 
	        if(event.keyCode == "13")    
	            {   
					$.ajax({
						url:"/sfm/dispatch/item/",
						type:"POST",
						data:{'dep':dep,'item':item},
						dataType:"json",
						success:function(ret){	
							parameters(ret);
							routings(ret);
							},
					});	
					return false;  
	            }  
        	});


	    $('#lotsize').on('blur',function(event){ 
	    	$('#lotsize').cbNum();
     	   });


	    $('#lotqty').on('blur',function(event){ 
	    	$('#lotqty').cbNum();
	    	var a =parseInt($("#dispatchqty").val());
	    	var b =parseInt($(this).val());
	    	if(b>a){ $(this).val(a); };
        	});


	    $('#dispatchqty').on('blur',function(event){  
	    	$('#dispatchqty').cbNum();
	        var a =parseInt($("#dispatchqty").val());
			var b =parseInt($("#startqty").text().substring(4));  //取第4位后的工单投料数
			var c = a / b ;
			var d=parseInt($("#dispatchinfo").text().substring(6));  //取第6位后的累积派单数

			if(d>b){
				$('#dispatchqty').val(0);
			}else if((a+d)>b){
				$('#dispatchqty').val(b-d);
				alert("累计派单数已超过工单投料数！");
			};
  
				$("#BOM").find("tbody").each(function(){
				    var tdArr = $(this).children();
				    var required = tdArr.eq(3).text();
				    var issued=Math.ceil(required * c);    //向上取整
				    tdArr.eq(1).find("input").val(issued);
				  });
	        });


	    $('#dispatchqty').on('keypress',function(event){  
	        if(event.keyCode == "13"){ 

	        	return false;  
         	   }  
	    	});


	    $('#lotqty').on('keypress',function(event){  
	        if(event.keyCode == "13"){ 

	        	return false;  
            }  
	  	  });


	    $('#lotsize').on('keypress',function(event){  
	        if(event.keyCode == "13"){ 
	        	return false;  
    	        }  
		    });

		//手动派单
	    $('#dispatchsn').on('keypress',function(event){ 	    	

	        if(event.keyCode == 13){
    		    	var sn = $("#dispatchsn").val().trim();
			    	var lotsize = parseInt($("#lotsize").val(),10);   //十进制整数
				    var lotqty = parseInt($("#lotqty").val(),10);
				    var dispatchqty = parseInt($("#dispatchqty").val(),10);
				    var wodisqty=parseInt($("#dispatchinfo").text().substring(6));   //累积派单
			    	var cell = $("#dispatchcell").val();
			    	var operation=$("#dispatchoperation").val();
			    	var time=getFormatDate();
			    	rows+=1
			    	var text1 = "<tr><td>"+ sn +"</td><td>"+ lotsize +"</td><td>"+ cell +"</td><td>"+ operation +"</td><td>"+ time +"</td>";  
	    				text1 += "<td class='text-center'><label class='css-input css-checkbox css-checkbox-primary'><input type='checkbox' id='row_"+ rows +"' name='row_"+ rows +"' checked='true'><span></span></label></td></tr>";
					var sns=eval(JSON.stringify(snjson()));  //已刷入号！

					$.ajax({
						url:"/sfm/dispatch/sn/",
						type:"POST",
						data:{'time':time,'sn':sn},
						dataType:"json",
						success:function(ret){	
								 var objs = eval(ret.sns);
								 var judgs = 0;  //验证SN重复刷入
			 						$.each(sns,function(i,item){
										//alert(item.sn + ':' +sn) ;
										if(item.sn == sn){
											//alert(sn + "重复刷入！");
											judgs = 1;
										};
									});

								 if(objs==0&&judgs==0){
									$('#SNID').append(text1);
									$('#lotqty').val(lotqty+1); 
									$('#dispatchqty').val(lotsize+dispatchqty);
									//$('#dispatchsn').empty();
									//更新BOM用料
									var a = $("#dispatchqty").val();
									var b = $("#startqty").text().substring(4); //取第4位后的数字
									var c = a / b ;
									$("#BOM").find("tbody").each(function(){
									    var tdArr = $(this).children();
									    var required = tdArr.eq(3).text();
									    var issued=Math.ceil(required * c);    //向上取整
										//tdArr.eq(1).find("input").empty();
									    tdArr.eq(1).find("input").val(issued);//attr("value",issued);
								  	});
						
								 }else{

								 	alert('SN重复派单：'+ sn );

								 };				 																	
							},
					});	

					$('#dispatchsn').val("");
					$("#dispatchsn").focus();		
					return false;					
     	       }  
  	      });

	    //编码方式
		$("#sntype").change(function(){
			$('#triduuid').empty();
			$('#triduuid').append(uuid());
			$('#SNID').find("tr").not(':eq(0)').remove(); 
			var sntype = $("#sntype").prop('checked');
	        if(sntype==true){
	        	$("#dispatchsn").attr("disabled",true); 
	        	$("#lotsize").attr("disabled",true); 
	        	$("#lotqty").attr("disabled",false); 
	        	$("#dispatchqty").attr("disabled",false); 
	        	$('#lotsize').val("0");
	        	$("#dispatchqty").val("0");
	        	$('#lotqty').val("0");
	        	//$("#lotqty").attr("value",0); 

	        }else{
	        	$("#dispatchsn").attr("disabled",false);
	        	$("#lotsize").attr("disabled",false); 	        	
	        	$("#lotqty").attr("disabled",true); 
	        	$("#dispatchqty").attr("disabled",true); 
	        	$('#lotsize').val("1"); 
	        	$("#dispatchqty").val("0"); 
	        	$('#lotqty').val("0");
	        	
	   	     };
			});

		$("#wostates").change(function(){
			var wostate = $("#wostates").prop('checked');
	        var label=document.getElementById("wslabel"); 
	        if(wostate==true){		 
			    //$("wslabel").html("生产中"); 
	        }else{
	        	//$("wslabel").html("已完工");  
	  	      };
			});

		//增加用料
		$("#bomadd").click(function(){
			var tb=$('#BOM').find('tbody');
			var text="<tr><td><input class='form-control' type='text' name='component' value=''></td><td><input class='form-control' type='text' name='qty'></td><td><input class='form-control' type='text' name='lot' ></td><td></td><td></td><td></td><td></td></tr>";
			tb.append(text);
			});

		//增加参数
		$("#routeadd").click(function(){
			var tb=$('#ROUTING').find('tbody');
			var text="<tr><td><input class='form-control' type='text' name='step'></td><td></td><td><input class='form-control' type='text' name='process'></td><td></td><td></td><td><input class='form-control' type='text' name='spec'></td></tr>";
			tb.append(text);
			});

	    //隐藏产品信息
		$("#productinfo").click(function(){
			hideshow('#productdata');
			});

	    //隐藏Routing失效信息
		$("#routinginfo").click(function(){
			hideshow('#routingdata');
			});

	    //隐藏用料信息
		$("#bominfo").click(function(){
			hideshow('#bomdata');
			});

	    //隐藏参数信息
		$("#parameterinfo").click(function(){
			hideshow('#parameterdata');
			});


})
//主程序结束



var HTMLStart=function(){

    var dep = $("#dispatchdep").val();
	$.ajax({
			url:"/sfm/dispatch/dep/",
			type:"POST",
			data:{'dep':dep,'sle':'1'},
			dataType:"json",
			success:function(ret){	
				cells(ret);
				var cell=$("#dispatchcell").val();					
				$.ajax({
						url:"/sfm/dispatch/cell/",
						type:"POST",
						data:{'cell':cell,'sle':'1'},
						dataType:"json",
						success:function(ret){	
							operations(ret);
						},
				});							
			},
		});		
	};



//隐藏
function hideshow(ret){

		var node=$(ret);
		if(node.is(':hidden')){　　
		　　node.show();　
		}else{
		　　node.hide();
		}
	
};

function woinfos(ret){
		$('#startqty').empty();       //label
		$('#completeqty').empty();
		$('#item').val("");           //input
		$('#itemdesc').empty();
		$('#itemspec').empty();
		$('#daterange1').val("");
		$('#daterange2').val("");
		$('#dispatchqty').val("0");
		$('#lotqty').val("0");
		$('#lotsize').val("0");
		$('#dispatchinfo').empty();	
		var a=0;	
		
		objs2 = eval(ret.SQ);
		$.each(objs2,function(i,item){	
			a=item.SQ;		
			$('#dispatchinfo').append('累计派单数:'+a);
		});

		objs = eval(ret.woinfos);
		$.each(objs,function(i,item){			
			$('#startqty').append('投料数:'+ item.startqty);
			$('#completeqty').append('完工数:'+item.completeqty);
			$('#item').val(item.item);
			$('#itemdesc').append('产品描述：'+item.itemdesc);
			$('#itemspec').append('产品规格：'+item.itemspec);
			$('#daterange1').val(item.startdate);
			$('#daterange2').val(item.enddate);
			if(a>item.wodif){ $('#dispatchqty').val(0); }else{ $('#dispatchqty').val(item.wodif-a); };  //投料数-完工数-派工数			  
			$('#lotqty').val('0');
			$('#lotsize').val('0');	
		});

		var b=$("#startqty").text().substring(4); //投入料
		if(a > b){alert("注意：此工单派单数已超过投料数！");};


};

function cells(ret){
		$('#dispatchcell').empty();
		objs = eval(ret.cells);
		$.each(objs,function(i,item){	
			var text = "<option  value= '" + item.code+ "' > "+ item.cell +" </option>";
			$("#dispatchcell").append(text);
		});

};

function operations(ret){
        $('#dispatchoperation').empty();
        $('#ERPoperation').empty();

        objs = eval(ret.operations);
        $.each(objs,function(i,item){           
            var text = "<option  value= '" + item.opcode+ "' > "+ item.opcode +'-'+item.operation +" </option>";
            $("#dispatchoperation").append(text);
        });

        eps= eval(ret.erps);
        $.each(eps,function(i,item){           
            $("#ERPoperation").attr('value',item.ERP);
        });

};


function poids(ret){
		$('#dispatchpoid').empty();
		$('#CRM').empty();
		$('#MRM').empty();
		$('#QRM').empty();
		$('#PRM').empty();

		objs = eval(ret.poids);
		if(jQuery.isEmptyObject(objs)){
			alert("请输入正确的部门或订单号或订单已关结");
			//return false;
		};
		$.each(objs,function(i,item){			
			var text1 = "<option  value= '" + item.poid+ "' > "+ item.poid +" </option>";
			var text2= "<option  value= '" + item.wo+ "' > "+ item.wo +" </option>";
			$("#dispatchpoid").append(text1);
			$("#dispatchwo").append(text2);
		});

		poinfo=eval(ret.poinfos);
		$.each(poinfo,function(i,item){	
			$('#CRM').append('客户要求：'+item.crm);
			$('#MRM').append('生产要求：'+item.mrm);
			$('#QRM').append('品质要求：'+item.qrm);
			$('#PRM').append('包装要求：'+item.prm);
		});
};

function wos(ret){
		$('#dispatchwo').empty();
		objs = eval(ret.wos);
		$.each(objs,function(i,item){			
			var text = "<option  value= '" + item.wo+ "' > "+ item.wo +" </option>";
			$("#dispatchwo").append(text);
		});
};

function boms(ret){
		$('#BOM').find("tbody").remove();
		objs=eval(ret.boms);
		var SQ = $("#startqty").text().substring(4); 
		var DQ = $("#dispatchqty").val();
		var P = DQ / SQ;
		//alert(SQ+DQ+ P);
		text1="<tbody>";
		$.each(objs,function(i,item){
			text1 += "<tr><td><input class='form-control' type='text' name='component' style='width:80px;' value='"+ item.component +"' ></td><td><input class='form-control' type='text' name='released' value="+   Math.ceil(item.required * P) +"></td><td><input class='form-control has-warning' type='text' name='lot'></td><td>"+ item.required +"</td><td>"+ item.issued +"</td><td>"+ item.released +"</td><td>"+ item.Comdesc +"</td></tr>";
		});
		text1 +="</tbody>";
		$('#BOM').append(text1);
};

function parameters(ret){		
		$('#CPN').empty();
		cuspn=eval(ret.cuspns);
		$.each(cuspn,function(i,item){
			$('#CPN').append('客户品号：'+item.CPN);
		});

		$('#PARAMETER').find("tbody").remove();
		objs = eval(ret.parameters);
		text1="<tbody>";
		$.each(objs,function(i,item){		
			text1 += "<tr><td>"+ item.parameter_id +"</td><td>"+ item.spec +"</td><td>"+ item.UCL +"</td><td>"+ item.CL +"</td><td>"+ item.LCL +"</td></tr>";	
		});
		text1 +="</tbody>";
		$('#PARAMETER').append(text1);
};


function routings(ret){
		$('#ROUTING').find("tbody").remove();
		objs = eval(ret.routings);
		text1="<tbody>";
		$.each(objs,function(i,item){	
			text1 += "<tr><td><input class='form-control' type='text' name='released' value="+ item.step +"></td><td>"+ item.operation_id +"</td><td><input class='form-control' type='text' name='released' value="+ item.pcode +"></td><td>"+ item.pname +"</td><td>"+ item.labor +"</td><td><input class='form-control' type='text' name='states'></td></tr>";		
		});
		text1 +="</tbody>";
		$('#ROUTING').append(text1);
};


function snlist(ret){
		$('#SNID').find("tr").not(':eq(0)').remove();
		objs = eval(ret.snlist);
		var text1="";
		var j=0;
		$.each(objs,function(i,item){		
			j+=1;
			text1 += "<tr><td class='font-w600 push-10'>"+ item.sn +"</td><td>"+ item.lotsize +"</td><td>"+ item.cell +"</td><td>"+ item.dispatch +"</td><td>"+ item.updatetime +"</td>";	
			text1 += "<td class='text-center'><label class='css-input css-checkbox css-checkbox-primary'><input type='checkbox' id='row_"+ j +"' name='row_"+ j +"'><span></span></label></td></tr>";

		});
		$('#SNID').append(text1);
};

function uuid() {  
    var s = [];  
    var hexDigits = "0123456789abcdef";  
    for (var i = 0; i < 36; i++) {  
        s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);  
    }  
    s[14] = "4";  // bits 12-15 of the time_hi_and_version field to 0010  
    s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);  // bits 6-7 of the clock_seq_hi_and_reserved to 01  
    s[8] = s[13] = s[18] = s[23] = "-";  
   
    var uuid = s.join("");  
    return uuid;  
}; 


function bomjson() {
            var array=[];
            var r = /^\+?[1-9][0-9]*$/;   //正整数
    		$("#BOM").find("tr").not(':eq(0)').each(function(){
			    var tdArr = $(this).children();
			    var json={};
			    var json = { component: "", qty: "",lot: "" };
			    json.component = tdArr.eq(0).find("input").val().trim();			    
			    json.qty=tdArr.eq(1).find("input").val().trim();
			    json.lot=tdArr.eq(2).find("input").val().trim();
			    //alert(json.component);
			    if(json.component.length!=0&&r.test(json.qty)){
			    	array.push(json);
			    };			    
		    });
            return array ;
    };


function snjson() {
            var array=[];
    		$("#SNID").find("tr").not(':eq(0)').each(function(){
			    var tdArr = $(this).children();
			    var json={};
			    var json = { sn: "", qty: 0,cell: "",ck:'false'};
			    json.sn = tdArr.eq(0).text().trim();			    
			    json.qty=tdArr.eq(1).text().trim();
			    json.cell=tdArr.eq(2).text().trim();
			    json.ck=tdArr.eq(5).find("input").prop('checked').toString();
    			
			    if(json.sn!=null && json.ck=='true'){
			    	array.push(json);
			    };	    
			});
            return array ;
    };


function routjson() {
            var array=[];
    		$("#ROUTING").find("tr").not(':eq(0)').each(function(){
			    var tdArr = $(this).children();
			    var json={};
			    var json = { step: "0", pcode: "",states: "" };
			    json.step=tdArr.eq(0).find("input").val().trim();			    
			    json.pcode=tdArr.eq(2).find("input").val().trim();
			    json.states=tdArr.eq(5).find("input").val().trim();  //制程说明

			    if(json.step!=null && json.pcode!=null){
			    	array.push(json);
			    };			    
		    });
            return array ;
    };

function getFormatDate(){    
    var nowDate = new Date();     
    var year = nowDate.getFullYear();    
    var month = nowDate.getMonth() + 1 < 10 ? "0" + (nowDate.getMonth() + 1) : nowDate.getMonth() + 1;    
    var date = nowDate.getDate() < 10 ? "0" + nowDate.getDate() : nowDate.getDate();    
    var hour = nowDate.getHours()< 10 ? "0" + nowDate.getHours() : nowDate.getHours();    
    var minute = nowDate.getMinutes()< 10 ? "0" + nowDate.getMinutes() : nowDate.getMinutes();    
    var second = nowDate.getSeconds()< 10 ? "0" + nowDate.getSeconds() : nowDate.getSeconds();    
    return year + "-" + month + "-" + date+" "+hour+":"+minute+":"+second;    
} 


//生成流程单页面列印
var snprint=function(ret){
	var objs = eval(ret.msns);
	var routs=eval(ret.routs);
	var params=eval(ret.params);
	var time=getFormatDate();
	var dep = $("#dispatchdep").val();

	var htmd='';
	
	var truthBeTold = window.confirm("确认打印，单击“确定”继续。单击“取消”停止。"); 

	$.each(routs,function(i,item){	
			var htmp='';
			$.each(params,function(j,jtem){	
					if(jtem.pcode_id==item.pcode && jtem.pmproperty==1){ htmp+= jtem.parameter_id+':(_____________)'+jtem.CL+jtem.spec+'\n; ';}
					else if(jtem.pcode_id==item.pcode){htmp+= jtem.parameter_id+':(_____________)'+jtem.LCL+'-'+jtem.UCL+jtem.spec+'\n; ';};
				});

			htmd+="<TR  style='height: 80px;'><TD>"+ item.operation_id+"</TD><TD>"+item.step+'.'+item.pname+"</TD><TD></TD><TD></TD><TD></TD><TD>"+ htmp +"</TD></TR>";
		});



	$.each(objs,function(i,item){	
				     
		var html = '';	
		    html+="<div style='height: 1200px;width:800px;'><div><h3 align='center'> HYC | MES 亿 源 通 光 电 科 技 有 限 公 司 </h3><h5 align='center'> "+dep+" 生 产 流 程 单 </h5><hr>" ;  
		    html+="<TABLE align='center' style='height: 90px;width:800px;'><tr><td>料号:</td><td><img id='itemcode' style='height: 90px;'/></td><td>流程单:</td><td><img id='sncode' style='height:90px;' /></td></tr></TABLE><TABLE align='center' style='height: 100px;width:800px;'><tr><td>工单："+item.wo+"</td><td>订单："+item.po+"</td><td>项次："+item.poid+"</td><td>数量："+item.lotsize+"</td></tr><tr><td>产线："+item.PL+"</td><td>Cell："+item.cell+"</td><td>工站："+item.operation+"</td><td>打印："+ time +"</td></tr></TABLE><table align='center' style='width:800px;'><tr><td>HYC-QR-IE-001 A/0</td></tr></table>" ;
		    html+="<TABLE align='center' border='3'  style='width:800px;border-collapse:collapse;'><THEAD style='height: 40px;'><TR><TH style='width: 40px;'>工站</TH><TH style='width: 80px;'>制程</TH><TH style='width: 80px;' text-align='center'>人员-机台</TH><TH style='width: 160px;'>日期-时间</TH><TH style='width: 160px;' >投入-产出</TH><TH style='width: 280px;'>参数记录</TH></TR></THEAD><TBODY>";
		    html=html+htmd+"</TBODY></TABLE><hr/><div align='left' id='foot'></div></div></div>" ; 

		    //alert(html);

			document.getElementById('TCARD').innerHTML=html;
			document.getElementById('foot').innerHTML = document.getElementById('productdata').innerHTML;
			$('#sncode').JsBarcode(item.sn);
			$('#itemcode').JsBarcode(item.item);
			if(truthBeTold){ $('#TCARD').print();({globalStyles:true,mediaPrint:false,stylesheet:null,});};										
			//document.getElementById('TCARD').innerHTML='';				
			});

	};
