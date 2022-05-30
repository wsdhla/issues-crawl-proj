package com.etoak.tian.stat;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

import java.net.URLDecoder;

@SpringBootApplication
@MapperScan({"com.etoak.tian.stat.mapper"})
public class IssuesStatisticsApplication {

    public static void main(String[] args) {
        ConfigurableApplicationContext context = SpringApplication.run(IssuesStatisticsApplication.class, args);
        String gitlabSession = context.getEnvironment().getProperty("crawl.login.gitlab_session");
        String lableDict = context.getEnvironment().getProperty("crawl.lable-dict");

        try {
            String pyPath = URLDecoder.decode(IssuesStatisticsApplication.class.getResource("/db/my-crawl.py").getPath().substring(1), "utf-8");
            System.out.println(pyPath);

            //Runtime.getRuntime().exec("cmd /k start");
            //Runtime.getRuntime().exec("cmd /k start copy C:\\Users\\wsdhla\\Desktop\\test.cmd  C:\\Users\\wsdhla\\Desktop\\abc");
            //Runtime.getRuntime().exec("cmd /k start cmd /k java -version ^&pause");
            //Runtime.getRuntime().exec("cmd /k start cmd /c java -version ^&pause");
            //Runtime.getRuntime().exec("cmd /k start cmd /c python D:/WorkSpace/005-program/IdeaProjects/crawl-test/issues-statistics/target/classes/db/my-crawl.py abc ^&pause");
            Runtime.getRuntime().exec("cmd /k start cmd /c python " + pyPath + " " + gitlabSession + " " + lableDict.replaceAll("\"", "\"\"\"") + " ^&pause");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
