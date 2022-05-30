package com.etoak.tian.stat.controller;

import com.etoak.tian.stat.mapper.IssuesStatisticsMapper;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.Resource;
import java.util.*;

@Controller
@RequestMapping("/issuestat")
public class IssuesStatisticsController {

    @Resource
    private IssuesStatisticsMapper issuesStatisticsMapper;

    @GetMapping("/index")
    public String main() {
        return "/index";
    }


    @GetMapping("/statQuery")
    @ResponseBody
    public Map<String, Object> statQuery() {
        List<Map> statBySuResultMap = issuesStatisticsMapper.statBySu();
        List<Map> statByStatusResultMap = issuesStatisticsMapper.statByStatus();
        List<Map> statByAssigneeResultMap = issuesStatisticsMapper.statByAssignee();

        Map<String, Object> statByAllAssigneeResultMap = new HashMap<>();
        List<String> allAssignee = issuesStatisticsMapper.getAllAssignee();
        List<Map> statByAllAssignee = issuesStatisticsMapper.statByAllAssignee();


        List newStatusData = new ArrayList();
        List openStatusData = new ArrayList();
        List reopenStatusData = new ArrayList();
        List fixedStatusData = new ArrayList();
        List submitStatusData = new ArrayList();


        for (String assignee: allAssignee) {
            Optional<Map> dataRow = statByAllAssignee.stream()
                    .filter(x -> assignee.equals((String) x.get("issue_assignee")) && "4状态-New".equals((String) x.get("issue_status")))
                    .findFirst();

            if (dataRow.isPresent()) {
                newStatusData.add(dataRow.get().get("value"));
            } else {
                newStatusData.add(0);
            }

            dataRow = statByAllAssignee.stream()
                    .filter(x -> assignee.equals((String) x.get("issue_assignee")) && "4状态-Open".equals((String) x.get("issue_status")))
                    .findFirst();

            if (dataRow.isPresent()) {
                openStatusData.add(dataRow.get().get("value"));
            } else {
                openStatusData.add(0);
            }

            dataRow = statByAllAssignee.stream()
                    .filter(x -> assignee.equals((String) x.get("issue_assignee")) && "4状态-再次出现".equals((String) x.get("issue_status")))
                    .findFirst();

            if (dataRow.isPresent()) {
                reopenStatusData.add(dataRow.get().get("value"));
            } else {
                reopenStatusData.add(0);
            }

            dataRow = statByAllAssignee.stream()
                    .filter(x -> assignee.equals((String) x.get("issue_assignee")) && "4状态-fixed".equals((String) x.get("issue_status")))
                    .findFirst();

            if (dataRow.isPresent()) {
                fixedStatusData.add(dataRow.get().get("value"));
            } else {
                fixedStatusData.add(0);
            }

            dataRow = statByAllAssignee.stream()
                    .filter(x -> assignee.equals((String) x.get("issue_assignee")) && "4状态-Submit".equals((String) x.get("issue_status")))
                    .findFirst();

            if (dataRow.isPresent()) {
                submitStatusData.add(dataRow.get().get("value"));
            } else {
                submitStatusData.add(0);
            }
        }


        statByAllAssigneeResultMap.put("allAssignee", allAssignee);
        statByAllAssigneeResultMap.put("statusNew", newStatusData);
        statByAllAssigneeResultMap.put("statusOpen", openStatusData);
        statByAllAssigneeResultMap.put("statusReopen", reopenStatusData);
        statByAllAssigneeResultMap.put("statusFixed", fixedStatusData);
        statByAllAssigneeResultMap.put("statusSubmit", submitStatusData);

        Map<String, Object> resultMap = new HashMap<>();
        resultMap.put("statBySU", statBySuResultMap);
        resultMap.put("statByStatus", statByStatusResultMap);
        resultMap.put("statByAssignee", statByAssigneeResultMap);
        resultMap.put("statByAssigneeBar", statByAllAssigneeResultMap);
        return resultMap;
    }
}
