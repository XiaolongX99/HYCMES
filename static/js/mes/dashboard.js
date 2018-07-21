//dashboard.jquery-2.0.3,2018-04-03

$(document).ready(function(){
    
	HTMLStart();

	$("#dep").change(function(){
        var a = $("#dep").val();
        var b = $("#cell").val();
		var c = $("#daterange1").val(); 
		var d = $("#daterange2").val();
        var e = $("#dailyselect").val();
		$.ajax({
				url:"/mes/dashboard/",
				type:"POST",
				data:{'dep':a,'cell':b,'std':c,'etd':d,'dst':e,'sle':'1'},
				dataType:"json",
				success:function(ret){	
					messum(ret);
					cells(ret);	
					cellsum(ret);
					datesum(ret);
                    fqcsum(ret);			
					
					},
				});		
			});
			
	$("#cell").change(function(){
        var a = $("#dep").val();
        var b = $("#cell").val();
		var c = $("#daterange1").val(); 
		var d = $("#daterange2").val();
        var e = $("#dailyselect").val();
		$.ajax({
				url:"/mes/dashboard/",
				type:"POST",
				data:{'dep':a,'cell':b,'std':c,'etd':d,'dst':e,'sle':'2'},
				success:function(ret){	
					messum(ret);
					cellsum(ret);
					datesum(ret);
                    fqcsum(ret);

					},
				});
			});
		
	$("#daterange1").change(function(){
        var a = $("#dep").val();
        var b = $("#cell").val();
		var c = $("#daterange1").val(); 
		var d = $("#daterange2").val();
        var e = $("#dailyselect").val();
		$.ajax({
				url:"/mes/dashboard/",
				type:"POST",
				data:{'dep':a,'cell':b,'std':c,'etd':d,'dst':e,'sle':'2'},
				success:function(ret){	
					messum(ret);
					cellsum(ret);
					datesum(ret);
                    fqcsum(ret);

					},
				});
			});

    $("#daterange2").change(function(){
        var a = $("#dep").val();
        var b = $("#cell").val();
        var c = $("#daterange1").val(); 
        var d = $("#daterange2").val();
        var e = $("#dailyselect").val();
        $.ajax({
                url:"/mes/dashboard/",
                type:"POST",
                data:{'dep':a,'cell':b,'std':c,'etd':d,'dst':e,'sle':'2'},
                success:function(ret){  
                    messum(ret);
                    cellsum(ret);
                    datesum(ret);
                    fqcsum(ret);

                    },
                });
            });

    $("#refresh_data").click(function(){
        var a = $("#dep").val();
        var b = $("#cell").val();
        var c = $("#daterange1").val(); 
        var d = $("#daterange2").val();
        var e = $("#dailyselect").val();        
        $.ajax({
                url:"/mes/dashboard/",
                type:"POST",
                data:{'dep':a,'cell':b,'std':c,'etd':d,'dst':e,'sle':'3'},
                success:function(ret){  
                    messum(ret);
                    cellsum(ret);
                    datesum(ret);
                    fqcsum(ret);
                    },
                });
            });

    $("#dailyselect").change(function(){
        var a = $("#dep").val();
        var b = $("#cell").val();
        var c = $("#daterange1").val(); 
        var d = $("#daterange2").val();
        var e = $("#dailyselect").val();
        $.ajax({
                url:"/mes/dashboard/",
                type:"POST",
                data:{'dep':a,'cell':b,'std':c,'etd':d,'dst':e,'sle':'2'},
                success:function(ret){  
                    messum(ret);
                    cellsum(ret);
                    datesum(ret);

                    },
                });
            });
}); 

function messum(ret){
		$('#FG').empty();
		$('#URT').empty();
		$('#EFY').empty();
		$('#ACR').empty();
		$('#UPPH').empty();
		$('#FCY').empty();
		$('#PPM').empty();			
		$('#FG').append(ret.FG);
		$('#URT').append(ret.URT);
		$('#EFY').append(ret.EFY);	
		$('#ACR').append(ret.ACR);	
		$('#UPPH').append(ret.UPPH);	
		$('#FCY').append(ret.FCY);
		$('#PPM').append(ret.PPM);
};

function cells(ret){
		$('#cell').empty();
		$("#cell").append("<option  value=CellSUM > CellSUM </option>");
		objcells = eval(ret.cells);
		$.each(objcells,function(i,item){			
			var text = "<option  value= '" + item.cell+ "' > "+ item.cell +" </option>";
			$("#cell").append(text);
		});
};

function cellsum(ret){
		$('#EFYURTACR').empty();
		$('#FGPQUPPH').empty();
		objcellsum=eval(ret.cellsum);
		text1="<thead><th class='font-w600 text-left' style='width: 70px;'>Cell</th><th class='font-w600 text-muted text-right' style='width: 70px;'>效率%</th><th class='font-w600 text-muted text-right' style='width: 70px;'>利用率%</th><th class='font-w600 text-success text-right' style='width: 70px;'>直通率%</th><th class='font-w600 text-warning text-right' style='width: 70px;'>达成率%</th></thead><tbody>";
		text2="<thead><th class='font-w600 text-left' style='width: 70px;'>Cell</th><th class='font-w600 text-muted text-right' style='width: 70px;'>完工数</th><th class='font-w600 text-muted text-right' style='width: 70px;'>人力</th><th class='font-w600 text-success text-right' style='width: 70px;'>UPPH</th><th class='font-w600 text-warning text-right' style='width: 70px;'>PPM</th></thead><tbody>";
		$.each(objcellsum,function(i,item){
			text1 += "<tr><td class='font-w600 text-left' style='width: 70px;'>"+ item.Cell +"</td><td class='font-w600 text-muted text-right' style='width: 70px;'>"+ item.EFY +"</td><td class='font-w600 text-muted text-right' style='width: 70px;'>"+ item.URT +"</td><td class='font-w600 text-success text-right' style='width: 70px;'>"+ item.FCY +"</td><td class='font-w600 text-warning text-right' style='width: 70px;'>"+ item.ACR +"</td></tr>";
			text2 += "<tr><td class='font-w600 text-left' style='width: 70px;'>"+ item.Cell +"</td><td class='font-w600 text-muted text-right' style='width: 70px;'>"+ item.FG +"</td><td class='font-w600 text-muted text-right' style='width: 70px;'>"+ item.PQ +"</td><td class='font-w600 text-success text-right' style='width: 70px;'>"+ item.UPPH +"</td><td class='font-w600 text-warning text-right' style='width: 70px;'>"+ item.PPM +"</td></tr>";
		});
		text1 +="</tbody>";
		text2 +="</tbody>";
		$('#EFYURTACR').append(text1);
		$('#FGPQUPPH').append(text2);		
};

function HTMLStart(){
        var a = $("#dep").val();
        var b = $("#cell").val();
		var c = $("#daterange1").val(); 
		var d = $("#daterange2").val();
        var e = $("#dailyselect").val();
        var f = $("#operation").val();
		$.ajax({
				url:"/mes/dashboard/",
				type:"POST",
				data:{'dep':a,'cell':b,'std':c,'etd':d,'dst':e,'operation':f},
				dataType:"json",
				success:function(ret){	
					messum(ret);
					cellsum(ret);
					datesum(ret);
                    fqcsum(ret);					
				},
		});
};

//颜色码生成
var getRandomColor = function(){   
  return  '#' +    
    (function(color){    
    return (color +=  '0123456789abcdef'[Math.floor(Math.random()*16)])    
      && (color.length == 6) ?  color : arguments.callee(color);    
  })('');    
} 

function fqcsum(ret){
    var FM = new Array();
    var Qty = new Array();
    var fqcdat="["
    objfqcfmsum=eval(ret.fqcfmsum);

    $.each(objfqcfmsum,function(i,item){
        FM.push(item.FM);
        Qty.push(item.Qty);
        fqcdat += "{value: "+ item.Qty +", color: '" + getRandomColor() + "', highlight: '" + getRandomColor() + "', label: '" + item.FM +"' }, "            
    });
    fqcdat = fqcdat.substr(0,fqcdat.length-2) +"]";
    //字符窜转JQ对像
    var fqcobj = eval ('{' + fqcdat + '}');
    //sumchart('#FQCsum',3,fqcobj,'','','');
    datechart('#FQCsum',2,FM,Qty,'','');

};

 function datesum(ret){
    	objdatesum=eval(ret.datesum);
        objtargetsum=eval(ret.targetsum);
    	var Xbar = new Array();
    	var EFY = new Array();
    	var URT = new Array();
    	var ACR = new Array();
    	var UPPH = new Array();
    	var FG = new Array();
    	var PQ = new Array();
    	var PPM = new Array();
    	var FCY = new Array();
        var PPM = new Array();
        var EFYucl = new Array(); //上限
        var EFYlcl = new Array(); //下限
        var URTlcl = new Array(); //下限
        var ACRlcl = new Array(); //下限
        var UPPHucl = new Array(); //上限
        var UPPHlcl = new Array(); //下限
        var PPMucl = new Array(); //上限

        //alert(objdatesum);
        $.each(objtargetsum,function(i,item){
            //alert(item.tcode);            
            switch(item.tcode){
                case 'ACR':         
                    ACRu=100*item.ucl;
                    ACRl=100*item.lcl;
                    break;
                case 'EFY':
                    EFYu=100*item.ucl;
                    EFYl=100*item.lcl;
                    break;
                case 'URT':
                    URTu=100*item.ucl;
                    URTl=100*item.lcl;
                    break;
                case 'UPPH':
                    UPPHu=item.ucl;
                    UPPHl=item.lcl;
                    break;
                case 'PPM':
                    PPMu=item.ucl;
                    PPMl=item.lcl;
                    break;
            }            
        });
        
    	$.each(objdatesum,function(i,item){
    		Xbar.push(item.WorkingDate);
    		EFY.push(item.EFY);
    		URT.push(item.URT);
    		ACR.push(item.ACR);
    		FCY.push(item.FCY);
    		FG.push(item.FG);
    		UPPH.push(item.UPPH);
    		PQ.push(item.PQ);
    		PPM.push(item.PPM);
            EFYucl.push(EFYu);
            EFYlcl.push(EFYl);
            URTlcl.push(URTl);
            ACRlcl.push(ACRl);
            UPPHucl.push(UPPHu);
            UPPHlcl.push(UPPHl);
            PPMucl.push(PPMu);
    	});
        //alert(PPMucl);
    	datechart('#EFYsum',1,Xbar,EFY,EFYucl,EFYlcl);
        datechart('#URTsum',1,Xbar,URT,'',URTlcl);
        datechart('#ACRsum',1,Xbar,ACR,'',ACRlcl);
    	datechart('#UPPHsum',1,Xbar,UPPH,UPPHucl,UPPHlcl);
    	datechart('#FGsum',1,Xbar,FG,'','');
    	datechart('#PQsum',1,Xbar,PQ,'','');
        datechart('#PPMsum',1,Xbar,PPM,PPMucl,'');    	
};

var $globalOptions = {
    scaleFontFamily: "'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif",
    scaleFontColor: '#999',
    scaleFontStyle: '600',
    tooltipTitleFontFamily: "'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif",
    tooltipCornerRadius: 3,
    maintainAspectRatio: false,
    responsive: true
};

function datechart(cht,chy,xba,da1,da2,da3){
        // Get Chart Container
        var $dashChartLinesCon  = jQuery(cht)[0].getContext('2d');
        // Set Chart and Chart Data variables
        var $dashChartLines, $dashChartLinesData;        
        // Lines/Bar/Radar Chart Data
        var $dashChartLinesData = {
            labels: xba,
            datasets: [
                {
                    label: 'UCL',
                    fillColor: 'rgba(100, 100, 100, .07)',
                    strokeColor: 'rgba(100, 100, 100, .25)',
                    pointColor: 'rgba(100, 100, 100, .25)',
                    pointStrokeColor: '#fff',
                    pointHighlightFill: '#fff',
                    pointHighlightStroke: 'rgba(44, 52, 63, 1)',
                    data: da2
                },
                {
                    label: 'LCL',
                    fillColor: 'rgba(44, 52, 63, .07)',
                    strokeColor: 'rgba(44, 52, 63, .25)',
                    pointColor: 'rgba(44, 52, 63, .25)',
                    pointStrokeColor: '#fff',
                    pointHighlightFill: '#fff',
                    pointHighlightStroke: 'rgba(44, 52, 63, 1)',
                    data: da3
                },
                {
                    label: 'data1',
                    fillColor: 'rgba(255, 100, 0, .1)',
                    strokeColor: 'rgba(255, 100, 0, .55)',
                    pointColor: 'rgba(255, 100, 0, .55)',
                    pointStrokeColor: '#fff',
                    pointHighlightFill: '#fff',
                    pointHighlightStroke: 'rgba(255, 100, 0, 1)',
                    data: da1
                }
            ]
        };

        // Init Lines Chart
        switch(chy){
            case 1: 
                $dashChartLines = new Chart($dashChartLinesCon).Line($dashChartLinesData,$globalOptions);
                break;
            case 2: 
                $dashChartLines = new Chart($dashChartLinesCon).Bar($dashChartLinesData,$globalOptions);
                break;
            case 3: 
                $dashChartLines = new Chart($dashChartLinesCon).Radar($dashChartLinesData,$globalOptions);
                break;
        }
};

function sumchart(cht,chy,xba,da1,da2,da3){
        //alert(xba[0]);
        // Get Chart Container
        var $dashChartLinesCon  = jQuery(cht)[0].getContext('2d');
        // Set Chart and Chart Data variables
        var $dashChartLines, $dashChartLinesData;        
        // Polar/Pie/Donut Data
        var $dashChartLinesData = xba;
        // Init Lines Chart
        switch(chy){
            case 1: 
                $dashChartLines = new Chart($dashChartLinesCon).PolarArea($dashChartLinesData,$globalOptions);
                break;
            case 2: 
                $dashChartLines = new Chart($dashChartLinesCon).Pie($dashChartLinesData,$globalOptions);
                break;
            case 3: 
                $dashChartLines = new Chart($dashChartLinesCon).Doughnut($dashChartLinesData,$globalOptions);
                break;
        }
}

