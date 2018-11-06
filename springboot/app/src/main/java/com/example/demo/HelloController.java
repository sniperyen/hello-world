package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 测试控制器
 *
 * @author: @Daniel
 * @create: 2018-11-05-下午 20:00
 */
@RestController
public class HelloController {

    @Value("${company.name}")
    private String companyName;

    @Autowired
    private DatabaseProperties databaseProperties;

    @RequestMapping("/hello")
    private String hello() {
        return String.format("Hello Spring Boot, I am %s! \n Connect %s database .", companyName, databaseProperties.getType());
    }
}


