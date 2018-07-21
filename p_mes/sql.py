from django.db import connection

def trigger():

	sql="create trigger t_pcode on p_pdm_pcode after insert,update as DECLARE @sad INT,@pcd varchar(40) DECLARE @chg varchar(40) set @pcd=(select pcode from inserted) set @sad=(select case when max(states) is null then 1 else max(states)+1 end  from p_pdm_pcoderev where pcode=@pcd) if (@sad = 1) begin set @chg = '首次建立!' end ELSE begin set @chg = cast(@sad-1 as varchar(12))+'次修订' END insert into p_pdm_pcoderev select pcode,pname,labor,@chg,@sad,getdate() as updatetime,updatename from inserted"
	connection.cursor().execute(sql)

