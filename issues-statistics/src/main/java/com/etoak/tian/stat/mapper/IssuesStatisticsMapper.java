package com.etoak.tian.stat.mapper;

import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;

@Repository
public interface IssuesStatisticsMapper {
    @Select("select issue_su as name, count(1) as value from T_issues group by issue_su")
    List<Map> statBySu();

    @Select("select issue_status as name, count(1) as value from T_issues group by issue_status")
    List<Map> statByStatus();

    @Select("select issue_assignee as name, count(1) as value from T_issues group by issue_assignee")
    List<Map> statByAssignee();

    @Select("select issue_assignee as name from T_issues group by issue_assignee order by issue_assignee")
    List<String> getAllAssignee();

    @Select("select issue_assignee,issue_status,count(1) as value from T_issues GROUP BY issue_assignee,issue_status ORDER BY issue_assignee,issue_status")
    List<Map> statByAllAssignee();
}
