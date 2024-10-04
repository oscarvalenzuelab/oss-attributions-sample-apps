package com.xpertians.sample;

import com.google.gson.Gson;
import org.apache.commons.lang3.StringUtils;

public class App {
    public static void main(String[] args) {
        // Test Gson
        Gson gson = new Gson();
        String json = gson.toJson(new App());
        System.out.println("Serialized App to JSON: " + json);

        // Test Apache Commons Lang
        System.out.println("Is the string empty? " + StringUtils.isEmpty(json));
    }
}
