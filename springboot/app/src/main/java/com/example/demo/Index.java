package com.example.demo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import java.text.DateFormat;
import java.util.Date;


@Controller
public class Index {

    @Value("${company.name}")
    private String companyName;

    @RequestMapping("/index")
    public String index(Model m) {
        m.addAttribute("now", DateFormat.getDateInstance().format(new Date()));
        m.addAttribute("companyName", companyName);
        return "index";
    }
}
