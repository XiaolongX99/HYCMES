//transfer.jquery-2.0.3,2018-06-20

$(document).ready(function(){	

		HTMLStart();

		$("#transfer").click(function(){
		    var dep = $("#DEP").val();
		    var cell = $("#CELL").val();
		    var operation = $("#OPERATION").val();  	//转出站
		    var inoperation = $("#INOPERATION").val();  //转入站
		    var group = $("#GROUP").val();
		    var po = $("#dispatchpo").val();
		    var poid = $("#dispatchpoid").val();
		    var wo = $("#dispatchwo").val();
		    var item = $("#item").val();
		    var trid = uuid();
		    var wdate = $("#WDATE").val();
		    var processs=JSON.stringify($('#PROCESS').val());       //多选制程
		    var operators=JSON.stringify($('#OPERATOR').val());     //多选人员

	    	var lotsize = parseInt($("#LOTSIZE").val());
		    var inputqty =parseInt($("#inputqty").val());
		    var passqty = parseInt($("#passqty").val());  
		    var failqty = parseInt($("#failqty").val());     //多项数量
		    var failmodels = JSON.stringify($("#FAILMODEL").val()); //多选失效模式
		    var faildesc= $("#faildesc").val();  
		    var distates = $("#distates").val();

		    var sntype = $("#sntype").prop('checked');   //移转模式Lot/Batch
		    var boms=JSON.stringify(bomjson());		    
		    var operationpro=$("#operationpro").val();  //工作参数		    

		    var reg=new RegExp('dispatch');  //派工站参数

		    if (reg.test(operationpro)){ 
		    	var parameters=JSON.stringify(parameterjson(1));
		    	var pro=1; 
		    }else{
		    	var parameters=JSON.stringify(parameterjson(0));
		    	var pro=0;
		    };

//alert(processs);
//return false;

		    if(sntype==true){
		    	var sns=$("#transfersn").val();      //lot模式
		    }else{
		    	var sns=JSON.stringify(snjson());    //batch模式
		    };

		    if(operation==inoperation){
		    	var trstates=0;   //站内移转，未完工; 
		    }else if(operation.substring(1) > inoperation.substring(1) && inoperation!='Closed'){
		    	var trstates = -1;  //向前站移转，批失效；
		    		distates = parseInt(distates) + 1;   //更新流程单状态
		    }else{
		    	var trstates=1;   //向后站移转，完工待检
		    };

//alert(inputqty+':'+lotsize);
			/*
		    if(trstates!=0 && inputqty < lotsize && sntype==true){
		    	var truthBeTold = window.confirm("该SN没有全部完工，确定要转入下站，单击“确定”继续。单击“取消”停止。"); 
		    	if (truthBeTold) { 
		    		return true;
		    	}else{
	    			//alert("该SN没有全部完工，不能转入下站");
			        $("#distates").val(0);
			        $("#LOTSIZE").val(0);
		    		return false;
		    	};
		    };
		    */

				$.ajax({
					url:"/sfm/transfer/transfer/",
					type:"POST",
					data:{'dep':dep,'cell':cell,'operation':operation,'inoperation':inoperation,'group':group,'po':po,'poid':poid,'wo':wo,'item':item,'trid':trid,'wdate':wdate,'processs':processs,'operators':operators,'inputqty':inputqty,'passqty':passqty,'failqty':failqty,'failmodels':failmodels,'faildesc':faildesc,'sntype':sntype,'distates':distates,'parameters':parameters,'boms':boms,'sns':sns,'pro':pro,'trstates':trstates},
					dataType:"json",
					success:function(ret){
				        $('#transfersn').val("");
				        $("#distates").val(0);
				        $("#LOTSIZE").val(0);
				        $('#inputqty').val(0);
				        $('#passqty').val(0);
				        $('#failqty').val(0);
				        $('#faildesc').val("");
				        $('#FAILMODEL').val("").select2();
				        $('#PARAMETER').find("tbody").remove();
				        $('#BOM').find("tbody").remove();
				        snlist(ret);					

						if (sntype==true){	
							alert('完成Lot移转， 良品:'+ passqty+'， 失效:' + failqty );

						}else{
							$('#transferlist').find("tbody").empty();							
							alert('完成Batch移转， 良品:'+ passqty+'， 失效:' + failqty );

						};
					},
				});	
			  //return false;	
		});

		$("#DEP").change(function(){	        
	        $('#transfersn').val("");
	        $("#distates").val(0);
	        $('#inputqty').val(0);
	        $('#passqty').val(0);
	        $('#failqty').val(0);
			$('#snlist').find("tbody").empty();
	        $('#dispatchpoid').empty();
	        $('#dispatchwo').empty();
	        var dep = $("#DEP").val();

			$.ajax({
					url:"/sfm/transfer/dep/",
					type:"POST",
					data:{'dep':dep,'sle':'1'},
					dataType:"json",
					success:function(ret){	
						cells(ret);	
						inoperations(ret);					
						var cell=$("#CELL").val();												
						$.ajax({
								url:"/sfm/transfer/cell/",
								type:"POST",
								data:{'cell':cell,'sle':'1'},
								dataType:"json",
								success:function(ret){	
									operations(ret);									
									groups(ret);
									var operation = $("#OPERATION").val();
									operationselect(operation);
									var group = $("#GROUP").val();								

									$.ajax({
											url:"/sfm/transfer/group/",
											type:"POST",
											data:{'cell':cell,'operation':operation,'group':group,'sle':'1'},
											dataType:"json",
											success:function(ret){	
												operators(ret);	
											},
									});	

									$.ajax({
											url:"/sfm/transfer/operation/",
											type:"POST",
											data:{'operation':operation,'sle':'1'},
											dataType:"json",
											success:function(ret){	
												processs(ret);
												failmodels(ret);
												operationpros(ret);

											},
									});		
								},
						});	
						
					},
			});		
		});


		$("#CELL").change(function(){
	        $('#transfersn').val("");
	        $("#distates").val(0);
	        $('#inputqty').val(0);
	        $('#passqty').val(0);
	        $('#failqty').val(0);
			$('#snlist').find("tbody").empty();
	        var cell = $("#CELL").val();
			$.ajax({
					url:"/sfm/transfer/cell/",
					type:"POST",
					data:{'cell':cell,'sle':'1'},
					dataType:"json",
					success:function(ret){	
						operations(ret);
						groups(ret);
						var operation = $("#OPERATION").val();
						operationselect(operation);
						var group = $("#GROUP").val();
						//operation
						$.ajax({
								url:"/sfm/transfer/operation/",
								type:"POST",
								data:{'operation':operation,'sle':'1'},
								dataType:"json",
								success:function(ret){	
									processs(ret);
									failmodels(ret);
									operationpros(ret);	
								},
						});	
						//group
						$.ajax({
								url:"/sfm/transfer/group/",
								type:"POST",
								data:{'cell':cell,'operation':operation,'group':group,'sle':'1'},
								dataType:"json",
								success:function(ret){	
									operators(ret);	
								},
						});	

					},
			});		
		});


		$("#OPERATION").change(function(){
	        $('#transfersn').val("");
	        $("#distates").val(0);
	        $('#inputqty').val(0);
	        $('#passqty').val(0);
	        $('#failqty').val(0);
			$('#snlist').find("tbody").empty();
	        var cell = $("#CELL").val();
	        var operation = $("#OPERATION").val();
	        operationselect(operation);

			$.ajax({
					url:"/sfm/transfer/operation/",
					type:"POST",
					data:{'operation':operation,'sle':'1'},
					dataType:"json",
					success:function(ret){	
						processs(ret);
						failmodels(ret);
						operationpros(ret);
						var group = $("#GROUP").val();
						$.ajax({
								url:"/sfm/transfer/group/",
								type:"POST",
								data:{'cell':cell,'operation':operation,'group':group,'sle':'1'},
								dataType:"json",
								success:function(ret){	
									operators(ret);	
								},
						});	

					},
			});		
		});


		$("#GROUP").change(function(){
	        $('#transfersn').val("");
	        $("#distates").val(0);
	        $('#inputqty').val(0);
	        $('#passqty').val(0);
	        $('#failqty').val(0);
			//$('#snlist').find("tbody").empty();
	        var cell = $("#CELL").val();
	        var operation = $("#OPERATION").val();
	        operationselect(operation);
	        var group = $("#GROUP").val();
			$.ajax({
					url:"/sfm/transfer/group/",
					type:"POST",
					data:{'cell':cell,'operation':operation,'group':group,'sle':'1'},
					dataType:"json",
					success:function(ret){	
						operators(ret);	
					},
			});		
		});


	    $('#dispatchpo').on('blur',function(event){  	    
	        $('#transfersn').val("");
	        $("#distates").val(0);
	        $('#inputqty').val(0);
	        $('#passqty').val(0);
	        $('#failqty').val(0);
		    var dep = $("#DEP").val();
		    var cell = $("#CELL").val();
		    var erp = $("#ERPoperation").val();
		    var po = $("#dispatchpo").val();
		    var wostate = $("#wostates").prop('checked');

	        //if(event.keyCode == "13"){ 
					$.ajax({
						url:"/sfm/transfer/po/",
						type:"POST",
						data:{'dep':dep,'cell':cell,'erp':erp,'po':po,'sle':wostate},
						dataType:"json",
						success:function(ret){	
							poids(ret);
						    var poid = $("#dispatchpoid").val();
							$.ajax({
									url:"/sfm/transfer/poid/",
									type:"POST",
									data:{'dep':dep,'cell':cell,'erp':erp,'po':po,'poid':poid,'sle':wostate},
									dataType:"json",
									success:function(ret){	
										wos(ret);
										var wo = $("#dispatchwo").val();
										var operation = $("#OPERATION").val(); 
										$.ajax({
												url:"/sfm/transfer/wo/",
												type:"POST",
												data:{'dep':dep,'wo':wo,'operation':operation,'sle':wostate},
												dataType:"json",
												success:function(ret){	
													woinfos(ret);
													boms(ret);
													snlist(ret);
													var item = $("#item").val();													
													$.ajax({
														url:"/sfm/transfer/item/",
														type:"POST",
														data:{'dep':dep,'item':item,'operation':operation},
														dataType:"json",
														success:function(ret){	
															//parameters(ret);
															processs(ret);
															$("#item").attr("disabled",true); 
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
	        $('#transfersn').val("");
	        $("#distates").val(0);
	        $('#inputqty').val(0);
	        $('#passqty').val(0);
	        $('#failqty').val(0);
			//$('#snlist').find("tbody").empty();			
		    var dep = $("#DEP").val();
		    var cell = $("#CELL").val();
		    var erp = $("#ERPoperation").val();
		    var po = $("#dispatchpo").val();
		    var poid = $("#dispatchpoid").val();
		    var wostate = $("#wostates").prop('checked');

			$.ajax({
					url:"/sfm/transfer/poid/",
					type:"POST",
					data:{'dep':dep,'cell':cell,'erp':erp,'po':po,'poid':poid,'sle':wostate},
					dataType:"json",
					success:function(ret){	
						wos(ret);
						var wo = $("#dispatchwo").val();
						var operation = $("#OPERATION").val();
						$.ajax({
							url:"/sfm/transfer/wo/",
							type:"POST",
							data:{'dep':dep,'wo':wo,'operation':operation,'sle':wostate},
							dataType:"json",
							success:function(ret){	
								woinfos(ret);
								boms(ret);	
								snlist(ret);
								var item = $("#item").val();
								var operation = $("#OPERATION").val(); 
								$.ajax({
									url:"/sfm/transfer/item/",
									type:"POST",
									data:{'dep':dep,'item':item,'operation':operation},
									dataType:"json",
									success:function(ret){	
										//parameters(ret);
										processs(ret);
									},
								});	
							},
						});		
					},
				});		
			});
   
	    $('#dispatchwo').change(function(){  
	        $('#transfersn').val("");
	        $("#distates").val(0);
	        $('#inputqty').val(0);
	        $('#passqty').val(0);
	        $('#failqty').val(0);
			//$('#snlist').find("tbody").empty();
		    var dep = $("#DEP").val();
			var wo = $("#dispatchwo").val();
		    var wostate = $("#wostates").prop('checked');
		    var operation = $("#OPERATION").val(); 
			$.ajax({
					url:"/sfm/transfer/wo/",
					type:"POST",
					data:{'dep':dep,'wo':wo,'operation':operation,'sle':wostate},
					dataType:"json",
					success:function(ret){	
						woinfos(ret);
						boms(ret);
						snlist(ret);
						var item = $("#item").val();
						var operation = $("#OPERATION").val(); 
						$.ajax({
							url:"/sfm/transfer/item/",
							type:"POST",
							data:{'dep':dep,'item':item,'operation':operation},
							dataType:"json",
							success:function(ret){	
								//parameters(ret);
								processs(ret);
							},
						});	
					},
				});		
			});

	    $('#item').on('keypress',function(event){ 
	    	$('#item').cbNum();
	    	var dep = $("#DEP").val();
	    	var item = $("#item").val(); 
	    	var operation = $("#OPERATION").val();

	        if(event.keyCode == "13")    
	            {   
					$.ajax({
						url:"/sfm/transfer/item/",
						type:"POST",
						data:{'dep':dep,'item':item,'operation':operation},
						dataType:"json",
						success:function(ret){	
							//parameters(ret);
							processs(ret);
							},
					});	
					return false;  
	            }  
        });


	    //移转方式
		$("#sntype").change(function(){
	        $('#transfersn').val("");
	        $("#distates").val(0);
        	$('#inputqty').val(0);
        	$("#passqty").val(0);
        	$("#failqty").val(0);
        	$("#dispatchsn").val("");
        	$('#PARAMETER').find("tbody").remove();
        	$('#transferlist').find("tbody").remove();
			var sntype = $("#sntype").prop('checked');
			hideshow('#transferlist');

	        if(sntype==false){    
	        //batch	        	
	        	$("#inputqty").attr("disabled",true); 
	        	$("#passqty").attr("disabled",true); 
		        $("#DEP").attr("disabled",true); 
 			    $("#CELL").attr("disabled",true); 
		   	    $("#OPERATION").attr("disabled",true);  	
		        $("#INOPERATION").attr("disabled",true);
		        $("#GROUP").attr("disabled",true);
		        $("#WDATE").attr("disabled",true);    
		        $("#dispatchpo").attr("disabled",true); 
		        $("#dispatchpoid").attr("disabled",true); 
		        $("#dispatchwo").attr("disabled",true); 
		        $("#item").attr("disabled",true); 

	        }else{     
	        //lot        	
	        	$("#inputqty").attr("disabled",false); 
	        	$("#passqty").attr("disabled",false); 
		        $("#DEP").attr("disabled",false);
 			    $("#CELL").attr("disabled",false); 
		   	    $("#OPERATION").attr("disabled",false);  	
		        $("#INOPERATION").attr("disabled",false);
		        $("#GROUP").attr("disabled",false);
		        $("#WDATE").attr("disabled",false);     
		        $("#dispatchpo").attr("disabled",false); 
		        $("#dispatchpoid").attr("disabled",false); 
		        $("#dispatchwo").attr("disabled",false); 
		        $("#item").attr("disabled",false); 
 	        	                                

	        };

		});


		//增加用料
		$("#bomadd").click(function(){
			var tb=$('#BOM').find('tbody');
			var text="<tr><td><input class='form-control' type='text' value=''></td><td><input class='form-control' type='text' value=''></td><td><input class='form-control' type='text' value='' ></td><td><input class='form-control' type='text' value=''></td><td>品名</td></tr>";
			tb.append(text);
		});


		//增加参数
		$("#parameteradd").click(function(){
			var tb=$("#PARAMETER").find('tbody');
			var text="<tr><td><input class='form-control' type='text' value=''></td><td><input class='form-control' type='text' value=''></td><td><input class='form-control' type='text' value='' ></td><td>规格</td>";
			text += "<td class='text-center'><label class='css-input css-checkbox css-checkbox-primary'><input type='checkbox' ><span></span></label></td></tr>";
			tb.append(text);
		});

	    //隐藏产品信息
		$("#productinfo").click(function(){

			hideshow('#productdata');

		});

	    //隐藏失效信息
		$("#failinfo").click(function(){

			hideshow('#faildata');

		});

	    //隐藏用料信息
		$("#bominfo").click(function(){

			hideshow('#bomdata');

		});

	    //隐藏参数信息
		$("#parameterinfo").click(function(){

			hideshow('#parameterdata');

		});

	    //隐藏在制信息
		$("#snlistid").click(function(){

			hideshow('#snlist');

		});

		//刷入SN
	    $('#transfersn').on('blur',function(event){ 	    	
			//alert($('#transfersn').val());	
	        //if(event.keyCode == 13){
    		    	var sn = $("#transfersn").val().trim();
			    	var cell = $("#CELL").val();
			    	var operation=$('#OPERATION').val();
			    	var wo=$('#dispatchwo').val();
			    	var item = $("#item").val(); 
			    	var sntype = $("#sntype").prop('checked');
    			    var po = $("#dispatchpo").val();
	    			var poid = $("#dispatchpoid").val();
	    			var lot=po+poid.slice(-2);
	    			var processs=JSON.stringify($('#PROCESS').val()).replace(/\[/,'\(').replace(/\]/,'\)').replace(/\"/g,'\'');  

					$.ajax({
						url:"/sfm/transfer/sn/",
						type:"POST",
						data:{'sn':sn,'cell':cell,'operation':operation,'processs':processs,'lot':lot,'wo':wo,'item':item,'sntype':sntype},
						dataType:"json",
						success:function(ret){	
														
							 	var snv = eval(ret.sns);
							 	var sta = eval(ret.state);
								var objs = eval(ret.parameters);		//参数
								var maxsn=eval(ret.msn);	             //最大编码号
								var prsns=eval(ret.prsns);				//已记录产品SN
								var sns=eval(JSON.stringify(snjson()));   //已刷入SN
								var judge=0;

								 //alert(prsns);
								 if(sta==0){  //验证OK
									 	var SNQ=parseInt(snv[0].wip,10); 				//SN当站WIP
									 	var DISTA=parseInt(snv[0].distates);           //SN状态
										$('#LOTSIZE').val(SNQ);      			 //SN派单批量
										$('#distates').val(DISTA); 				//SN派工状态
											//Lot
											if(sntype==true){  
												$('#PARAMETER').find("tbody").remove();
												$('#inputqty').val(SNQ);
												$('#passqty').val(SNQ);
												$('#failqty').val(0);
											//Batch
											}else{ 
											  	$("#transfersn").val("");
											  	//验证刷入重号
						 						$.each(sns,function(i,item){
													if(item.sn == sn){
														$('#transfersn').stop();
														judge=1;
													};
												});

						 						if (judge!=1){
													var SIQ=parseInt($('#inputqty').val());  //累计投入
													var SPQ=parseInt($('#passqty').val());   //累积产出
													var FQ=parseInt($('#failqty').val().trim(),10);    //当前失效

													if(FQ>SNQ){
														$('#failqty').val(SNQ);
														FQ=SNQ;
														var PQ=0;
													 }else{
													 	var PQ=SNQ-FQ;
													 };												 //当前产出
													var FM=JSON.stringify($("#FAILMODEL").val());    //失效模式
													var FD= $("#faildesc").val().trim();            //失效模式
													var OP=JSON.stringify($('#OPERATOR').val());    //人员名单
													$('#inputqty').val(SIQ+SNQ);
													$('#passqty').val(SPQ+PQ);
													var text2="<tbody><tr><td>"+ sn +"</td><td>"+ PQ  +"</td><td>"+ FQ +"</td><td><input class='form-control' type='text' name='fm' value='"+ FM +"'></td></td><td><input class='form-control' type='text' name='fd' value='"+ FD +"'></td></td><td><input class='form-control' type='text' name='op' value='"+ OP +"'></td><td style='display:none'>"+ DISTA +"</td></tr></tbody>";
													$('#transferlist').append(text2);
												}else{
													alert("序号："+ sn +"重复刷入");

												};

											};

											//参数刷新
											if (judge!=1){
												var text1="<tbody>";
												$.each(objs,function(i,item){	

													if(item.pmproperty=='1'&&SNQ>1){
														 //通用参数
														 	text1 += "<tr><td><input class='form-control' type='text' name='psn' value='"+ sn +"'></td><td><input class='form-control' type='text' name='parameter' value='"+ item.parameter_id  +"'></td><td><input class='form-control' type='text' name='value'></td><td>"+ item.spec+':' + item.LCL +'_'+ item.UCL +"</td>";														
															text1 += "<td class='text-center'><label class='css-input css-checkbox css-checkbox-primary'><input type='checkbox' ><span></span></label></td></tr>";
													}else if(prsns!=0){ //已编码
														$.each(prsns,function(j,jtem){
															text1 += "<tr><td><input class='form-control' type='text' name='psn' value='"+ jtem.prsn +"'></td><td><input class='form-control' type='text' name='parameter' value='"+ item.parameter_id  +"'></td><td><input class='form-control' type='text' name='value'></td><td>"+ item.spec+':' + item.LCL +'_'+ item.UCL +"</td>";
															text1 += "<td class='text-center'><label class='css-input css-checkbox css-checkbox-primary'><input type='checkbox' ><span></span></label></td></tr>";
														});
													}else{  //新编码
														for (var i=maxsn+1;i<SNQ+maxsn+1;i++){
															//var FF=('00'+i.toString(16).toUpperCase()).slice(-2);   //两位16进制数
															var sid=sn.substring(0,9)+('00000'+i.toString(10)).slice(-5);   //5位10进制数
															//alert(sid);															
														 	text1 += "<tr><td><input class='form-control' type='text' name='psn' value='"+ sid +"'></td><td><input class='form-control' type='text' name='parameter' value='"+ item.parameter_id  +"'></td><td><input class='form-control' type='text' name='value'></td><td>"+ item.spec+':' + item.LCL +'_'+ item.UCL +"</td>";	
											 				text1 += "<td class='text-center'><label class='css-input css-checkbox css-checkbox-primary'><input type='checkbox' ><span></span></label></td></tr>";

														};
													};		

												});
												text1 +="</tbody>";
												$('#PARAMETER').append(text1);
											};
					
								 }else if(sta==1){
								 	alert(sn+'不在此工单中!');
								 }else if(sta==2){
								 	alert(sn+'不在当前工站!');
							     }else if(sta==3){
								 	alert('请选择正确的工站和工单!');
							     }else{
								 	alert(sn+'无派工记录!');
								 };										 
							},
					});						
					return false;
            //}  
        });



	    $('#inputqty').on('blur',function(event){ 
	    	$(this).cbNum();
	    	var a=$(this).val().length;
    		if(a==0){
    			$(this).val(0);
    			alert(this + "不能为空，可以为0！");
    		};   

	    	var sntype = $("#sntype").prop('checked');
		    	if(sntype==true){
		    		var iq=parseInt($('#inputqty').val().trim());
		    		var pq=parseInt($('#passqty').val().trim());
		    		var fq=parseInt($('#failqty').val().trim());
		    		var lot=parseInt($('#LOTSIZE').val());
					
					if(iq>lot){		    			
		    			//$('#inputqty').val(lot);
		    			$('#passqty').val(iq);
		    			$('#failqty').val(0);
		    			alert("投入数超过批量！");

		    		}else if(pq>iq){
		    			$('#passqty').val(iq);
		    			$('#failqty').val(0);
		    			alert("产出数超过投入数！");

	    			}else{
	    				$('#passqty').val(iq-fq);
			   		};
			   	};
            	return false;
        });


	    $('#passqty').on('blur',function(event){ 
	    	$(this).cbNum();
	    	var a=$(this).val().length;
    		if(a==0){
    			$(this).val(0);
    			alert(this + "不能为空，可以为0！");
    		};    	

	    	var sntype = $("#sntype").prop('checked');
		    	if(sntype==true){
		    		var iq=parseInt($('#inputqty').val().trim());
		    		var pq=parseInt($('#passqty').val().trim());
		    		var fq=parseInt($('#failqty').val().trim());
		    		var lot=parseInt($('#LOTSIZE').val());

					if(pq>lot){		    			
		    			$('#inputqty').val(pq);
		    			//$('#passqty').val(lot);
		    			$('#failqty').val(0);
		    			alert("产出数超过批量！");

		    		}else if(pq>iq){
		    			$('#inputqty').val(pq);
		    			$('#failqty').val(0);
		    			alert("失效数超过批量！");

	    			}else{
	    				$('#failqty').val(iq-pq);
			   		};
		   		};
            	return false;
        });


	    $('#failqty').on('blur',function(event){ 
	    	$(this).cbNum();
	    	var a=$(this).val().length;
    		if(a==0){
    			$(this).val(0);
    			alert(this + "不能为空，可以为0！");
    		};  

	    	var sntype = $("#sntype").prop('checked');
		    	if(sntype==true){
		    		var iq=parseInt($('#inputqty').val().trim());
		    		var pq=parseInt($('#passqty').val().trim());
		    		var fq=parseInt($('#failqty').val().trim());
		    		var lot=parseInt($('#LOTSIZE').val());
					
					if(fq>lot){		    			
		    			$('#inputqty').val(fq);
		    			$('#passqty').val(0);
		    			//$('#failqty').val(lot);
		    			alert("失效数超过批量！");

		    		}else if(fq>iq){
		    			$('#inputqty').val(fq);
		    			$('#passqty').val(0);
		    			alert("失效数超过批量！");

	    			}else{
	    				$('#passqty').val(iq-fq);
			   		};
				};
        	return false;
        });

});
//主程序结束

//启动复位
var HTMLStart=function(){
	        var dep = $("#DEP").val();
			$.ajax({
					url:"/sfm/transfer/dep/",
					type:"POST",
					data:{'dep':dep,'sle':'1'},
					dataType:"json",
					success:function(ret){	
						cells(ret);	
						inoperations(ret);					
						var cell=$("#CELL").val();												
						$.ajax({
								url:"/sfm/transfer/cell/",
								type:"POST",
								data:{'cell':cell,'sle':'1'},
								dataType:"json",
								success:function(ret){	
									operations(ret);									
									groups(ret);
									var operation = $("#OPERATION").val();
									operationselect(operation);
									var group = $("#GROUP").val();								

									$.ajax({
											url:"/sfm/transfer/group/",
											type:"POST",
											data:{'cell':cell,'operation':operation,'group':group,'sle':'1'},
											dataType:"json",
											success:function(ret){	
												operators(ret);	
											},
									});	

									$.ajax({
											url:"/sfm/transfer/operation/",
											type:"POST",
											data:{'operation':operation,'sle':'1'},
											dataType:"json",
											success:function(ret){	
												processs(ret);
												failmodels(ret);
												operationpros(ret);

											},
									});		
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

function operationselect(ret){

		opn=$("#INOPERATION option[value='"+ ret +"']").next().val();  //下一站
		$("#INOPERATION").val(opn);
	
};

function woinfos(ret){
		$('#startqty').empty();     //label
		$('#completeqty').empty();
		$('#item').val('');        //input
		$('#itemdesc').empty();
		$('#itemspec').empty();
		$('#WDATE').val('');
		$('#passqty').val('');
		$('#inputqty').val('');
		$('#transferinfo').empty();
		
		objs = eval(ret.woinfos);
		$.each(objs,function(i,item){			
			$('#startqty').append('投料数:'+ item.startqty);
			$('#completeqty').append('完工数:'+item.completeqty);
			$('#item').val(item.item);
			$('#itemdesc').append('产品描述：'+item.itemdesc);
			$('#itemspec').append('产品规格：'+item.itemspec);
			$('#WDATE').val(getFormatDate(2));
			$('#passqty').val('0');
			$('#inputqty').val('0');	
		});

		objs2 = eval(ret.SQ);
		$.each(objs2,function(i,item){			
			$('#dispatchinfo').append('累计派单数:'+item.SQ);
			var b = $("#startqty").text().substring(4);
			if(item.SQ > b){alert("注意：此工单派单数已超过投料数！");};

		});

};

function cells(ret){
		$('#CELL').empty();
		objs = eval(ret.cells);
		$.each(objs,function(i,item){	
			var text = "<option  value= '" + item.code+ "' > "+ item.cell +" </option>";
			$("#CELL").append(text);
		});
};

function operations(ret){
        $('#OPERATION').empty();
        $('#ERPoperation').val("");

        objs = eval(ret.operations);
        $.each(objs,function(i,item){           
            var text = "<option  value= '" + item.opcode+ "' > "+ item.opcode +'-'+item.operation +" </option>";
            $("#OPERATION").append(text);
        });

        eps= eval(ret.erps);
        $.each(eps,function(i,item){           
            $("#ERPoperation").val(item.ERP);
        });

};

function inoperations(ret){
        $('#INOPERATION').empty();
        
        objs = eval(ret.inoperations);
        $.each(objs,function(i,item){           
            var text = "<option  value= '" + item.opcode+ "' > "+ item.opcode+'-'+item.operation +" </option>";
            $("#INOPERATION").append(text);
        });
         	var text1 = "<option  value= 'Closed' > 完工 </option>";
         	//alert(text1);
        $("#INOPERATION").append(text1);
};

function groups(ret){
		$('#GROUP').empty();
		objs = eval(ret.groups);
		$.each(objs,function(i,item){	
			var text = "<option  value= '" + item.groupcode+ "' > "+ item.groupdesc +" </option>";
			$("#GROUP").append(text);
		});

};

function failmodels(ret){
		$('#FAILMODEL').empty();
		objs = eval(ret.failmodels);
		//alert(objs);
		$.each(objs,function(i,item){	
			var text = "<option  value= '" + item.failcode+ "' > "+ item.faildesc +" </option>";
			$("#FAILMODEL").append(text);
		});

};


function operators(ret){
		$('#OPERATOR').empty();
		objs = eval(ret.operators);
		$.each(objs,function(i,item){	
			if(item.AMT==1){ var text = "<option  value= '" + item.jn+ "' selected='true' > "+ item.jn+' : '+item.name +" </option>"; 
		      }else{var text = "<option  value= '" + item.jn+ "' > "+ item.jn +' : '+item.name +" </option>";}
			$("#OPERATOR").append(text);
		});

};

//作业制程
function processs(ret){
		$('#PROCESS').empty();
		objs = eval(ret.processs);
		$.each(objs,function(i,item){	
			var text = "<option  value= '" + item.pcode+ "' selected='true' > "+ item.pname +'：'+ item.labor+" </option>";
			$("#PROCESS").append(text);
		});
};

//工作参数
function operationpros(ret){
		$('#operationpro').val("");
		objs = eval(ret.operationpros);
		var text="";
		$.each(objs,function(i,item){	
			 text += "'"+ item.process_id +"',";		
		});
		$('#operationpro').val(text);
};

function poids(ret){
		$('#dispatchpoid').empty();
		$('#CRM').empty();
		$('#MRM').empty();
		$('#QRM').empty();
		$('#PRM').empty();

		objs = eval(ret.poids);
		if(jQuery.isEmptyObject(objs)){
			alert("请输入正确的部门或订单号");
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
		text1="<tbody>";
		$.each(objs,function(i,item){
			text1 += "<tr><td><input class='form-control' type='text' name='component' value='"+ item.component +"'></td><td><input class='form-control' type='text' name='lot'></td><td><input class='form-control' type='text' name='qty' ></td><td><input class='form-control' type='text' name='remark'></td><td>"+ item.Comdesc +"</td></tr>";
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
			 text1 += "<tr><td><input class='form-control' type='text' name='psn' value='"+ item.item +"'></td><td><input class='form-control' type='text' name='psn' value='"+ item.parameter_id  +"'></td><td><input class='form-control' type='text' name='value'></td><td>"+ item.spec+':' + item.LCL +'_'+ item.UCL +"</td><td><input class='form-control' type='text' name='mark'></td></tr>";	
		});
		text1 +="</tbody>";
		$('#PARAMETER').append(text1);
};


function routings(ret){
		$('#ROUTING').find("tbody").remove();
		objs = eval(ret.routings);
		var text1="<tbody>";
		$.each(objs,function(i,item){	
			 text1 += "<tr><td>"+ item.step +"</td><td>"+ item.parent_id +"</td><td>"+ item.pcode +"</td><td>"+ item.pname +"</td><td>"+ item.labor +"</td></tr>";		
		});
		text1 +="</tbody>";
		$('#ROUTING').append(text1);
};


function snlist(ret){
		$('#snlist').find("tbody").remove();
		objs = eval(ret.snlist);
		var text1="<tbody>";
		$.each(objs,function(i,item){
			 text1 += "<tr><td>"+ item.sn +"</td><td>"+ item.wip +"</td><td>"+ item.cell +"</td><td>"+ item.dispatch +"</td><td>"+ item.updatetime +"</td></tr>";	
		});
		text1 +="</tbody>";
		$('#snlist').append(text1);
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

var parameterjson=function(ret){
            var array=[];
    		$("#PARAMETER").find("tr").not(':eq(0)').each(function(){
			    var tdArr = $(this).children();
			    var json={};
			    var json = {  sn: "",parameter: "",pvalue: "",pdesc:"" };			    			    
			    json.sn=tdArr.eq(0).find("input").val().trim();
			    json.parameter = tdArr.eq(1).find("input").val().trim();
			    json.pvalue=tdArr.eq(2).find("input").val().trim();
			    json.pdesc=tdArr.eq(4).find("input").prop('checked').toString();

			    if(json.pvalue.length!=0||ret==1){ array.push(json); };		    			    
		    });
            return array ;
};

var bomjson=function() {
            var array=[];
    		$("#BOM").find("tr").not(':eq(0)').each(function(){
			    var tdArr = $(this).children();
			    var json={};
			    var json = { component:"", lot:"", failqty:0, faildesc:"" };
			    json.component = tdArr.eq(0).find("input").val().trim();			    
			    json.lot=tdArr.eq(1).find("input").val().trim();
			    json.failqty=tdArr.eq(2).find("input").val().trim();
			    json.faildesc=tdArr.eq(3).find("input").val().trim();

			    if(json.component.length!=0&&(json.lot.length!=0||json.failqty.length!=0)){ array.push(json); };
		    });
            return array ;
    };


function snjson() {
            var array=[];
    		$("#transferlist").find("tr").not(':eq(0)').each(function(){
			    var tdArr = $(this).children();
			    var json={};
			    var json = { sn: "", sn1: "",sn2: "",sn3:"",sn4:"",sn5:"" };
			    json.sn = tdArr.eq(0).text().trim();			    //sn
			    json.sn1=tdArr.eq(1).text().trim();                 //pass
			    json.sn2=tdArr.eq(2).text().trim();                 //fail
			    json.sn3=tdArr.eq(3).find("input").val();           //failmodel
			    json.sn4=tdArr.eq(4).find("input").val();           //faildesc
			    json.sn5=tdArr.eq(5).find("input").val();           //operator   
			    json.sn6=tdArr.eq(6).text();		       		    //distates  

			    if(json.sn.length!=0){  array.push(json); };	
			});
            return array ;
    };


function getFormatDate(ft){    
    var nowDate = new Date();     
    var year = nowDate.getFullYear();    
    var month = nowDate.getMonth() + 1 < 10 ? "0" + (nowDate.getMonth() + 1) : nowDate.getMonth() + 1;    
    var date = nowDate.getDate() < 10 ? "0" + nowDate.getDate() : nowDate.getDate();    
    var hour = nowDate.getHours()< 10 ? "0" + nowDate.getHours() : nowDate.getHours();    
    var minute = nowDate.getMinutes()< 10 ? "0" + nowDate.getMinutes() : nowDate.getMinutes();    
    var second = nowDate.getSeconds()< 10 ? "0" + nowDate.getSeconds() : nowDate.getSeconds(); 

	    switch(ft){
	    case 1: 
	        return year + "-" + month + "-" + date+" "+hour+":"+minute+":"+second; 
	        break;
	    case 2: 
	        return year + "-" + month + "-" + date;
	        break;
	    case 3: 
	        return year  + month  + date;
	        break;
	    }   
} 