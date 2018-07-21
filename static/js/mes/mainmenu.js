

var MENUStart=function(){
	var slev='1'
			$.ajax({
					url:"/",
					type:"POST",
					data:{'slev':slev},
					dataType:"json",
					success:function(ret){	
						//operations(ret);
						objs = eval(ret.menus);
						alert(objs);

					},
			});		
		};
};

jQuery(function(){

   MENUStart(); 

});