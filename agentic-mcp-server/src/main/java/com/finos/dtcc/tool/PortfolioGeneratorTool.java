package com.finos.dtcc.tool;

import com.finos.dtcc.model.response.PortfolioReportResponse;
import com.google.gson.Gson;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

import java.time.Duration;

@Slf4j
@Component
public class PortfolioGeneratorTool {

    private static final String URL = "http://52.34.242.123/generate_portfolio_report?message=";

    @Tool(name = "GeneratePortfolioReport", description = "Generates a portfolio report based on the provided message.")
    public PortfolioReportResponse generatePortfolioReport(String message) {
        log.info("Generating portfolio report with message: {}", message);

        OkHttpClient client = new OkHttpClient.Builder()
            .connectTimeout(Duration.ofMinutes(2))
            .readTimeout(Duration.ofMinutes(2))
            .writeTimeout(Duration.ofMinutes(2))
            .build();
        Request request = new Request.Builder().url(URL + message).build();
        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful() && response.body() != null) {
                String responseBody = response.body().string();
                log.info("Portfolio report generated successfully: {}", responseBody);
                Gson gson = new Gson();
                return gson.fromJson(responseBody, PortfolioReportResponse.class);
            } else {
                log.error("Failed to generate portfolio report: {}", response.message());
            }
        } catch (Exception e) {
            log.error("Error during portfolio report generation request: {}", e.getMessage());
        }
        return new PortfolioReportResponse("");
    }
}
