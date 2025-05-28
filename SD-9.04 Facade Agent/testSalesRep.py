from crew_sales_report import SalesReportCrew

SalesRep= SalesReportCrew()
results = SalesRep.kickoff("Quem mais vendeu? Verifique tambem se varios vendedores empataram. Se esse for o caso, me envie o nome de todos os vendedores")

print(results)