setwd('E:/myRproj/trunk/jd/')
#source("MySQLJDBC.R",encoding="UTF-8")
library(RJDBC)
info<-"jdbc:mysql://127.0.0.1:3306/jd?useUnicode=true&characterEncoding=utf-8"
drv <- JDBC("com.mysql.jdbc.Driver", "mysql-connector-java-jar-5.1.19.jar", "`")
channel <- dbConnect(drv, info,  "root", "chin")

#channel <- mysqlJDBC(mysql.conf="MySQL.xml",
#                     jdbcdrv="mysql-connector-java-jar-5.1.19.jar")

df<-dbGetQuery(channel,"select * from tb_jd_phone")


strsub<-function(x){
  x<-strsplit(x,'，|,')
  x<-sort(unique(unlist(x)))
  x<-paste(x,collapse=',')
  if(length(x)==0)x=''
  return(x)
}
strsub1<-function(x){
  x<-strsplit(x,'，|,| ')
  x<-sort(unique(unlist(x)))
  x<-paste(x,collapse=',')
  if(length(x)==0)x=''
  return(x)
}
ossub<-function(x){
  x<-gsub('安卓（Android）','Android',x)
  x<-gsub('苹果（IOS）','iOS',x)
  x<-gsub('微软（WindowsPhone）','WindowsPhone',x)
  return(x)
}


df$p_system<-unlist(sapply(df$p_system,strsub))
df$p_system<-unlist(sapply(df$p_system,ossub))
df$p_screenSize<-unlist(sapply(df$p_screenSize,strsub))
df$p_network<-unlist(sapply(df$p_network,strsub))
df$p_color<-unlist(sapply(df$p_color,strsub1))
df$p_CPU<-unlist(sapply(df$p_CPU,strsub))
df$p_special<-unlist(sapply(df$p_special,strsub))
df$jd_price<-as.double(df$jd_price)

weightsub<-function(x){
  if(substr(x,nchar(x)-1,nchar(x))=='kg'){
    x<-gsub('kg','',x)
    x<-as.double(x)*1000
  }
  else{
    x<-gsub('g','',x)
    x<-as.double(x)
  }
  return(x)  
}
df$p_weight<-unlist(sapply(df$p_weight,weightsub))
hist(df$p_weight)
price<-df$jd_price
price<-price[!is.na(price)]
hist(price,breaks = c(min(price),100,200,500,1000,1500,2000,2500,
                      3000,4000,5000,6000,max(price)))

sort(table(df[,'p_weight']))
sort(table(df[,'jd_price']))

df[df$jd_price>10000,]
tagsub<-function(x){
  if(nchar(x)>0){
    x<-unlist(strsplit(x,'\n|\\(|\\)'))
    x<-x[nchar(x)>0]
    tags<-cbind(tag_name=x[seq(1,length(x),2)],
                tag_freq=x[seq(2,length(x),2)])
  }
  else{tags=NA}

  return(tags)
}
write.csv(df,file='JDphone.csv',row.names=F)
p_tags<-lapply(df$p_tags,tagsub)
#p_comment<-lapply(df$p_comment,tagsub)
library(ggplot2)

addtime<-df$p_addtime
addmonth<-substr(addtime,1,7)
mon<-table(addmonth)[-1]
mons=data.frame(mon=names(mon),freq=mon[])
p <- ggplot(mons, aes(x=mon,y=freq,group=1))
p + geom_line()


