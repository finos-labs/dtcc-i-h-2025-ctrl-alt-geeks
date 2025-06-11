package com.finos.dtcc.tool;

import com.finos.dtcc.model.response.FraudDetectionResponse;
import com.google.gson.Gson;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class FraudDetectionTool {

    private static final String URL = "http://3.141.30.43/fraud_detection/predict/";

    @Tool(name = "FraudDetection", description = "Detects fraud for a given customer/client ID")
    public FraudDetectionResponse isFraud(String clientId) {
        log.info("Detecting fraud for the client id: {}", clientId);

        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url(URL + clientId).build();
        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful() && response.body() != null) {
                String responseBody = response.body().string();
                log.info("Fraud detection response for client {}: {}", clientId, responseBody);
                Gson gson = new Gson();
                return gson.fromJson(responseBody, FraudDetectionResponse.class);
            } else {
                log.error("Failed to detect fraud for client {}: {}", clientId, response.message());
            }
        } catch (Exception e) {
            log.error("Error during fraud detection request: {}", e.getMessage());
        }
        return new FraudDetectionResponse(clientId, false);
    }
}
