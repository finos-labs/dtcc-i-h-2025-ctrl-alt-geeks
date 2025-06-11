package com.finos.dtcc.tool;

import com.finos.dtcc.model.request.LeadProcessRequest;
import com.google.gson.Gson;
import lombok.extern.slf4j.Slf4j;
import okhttp3.*;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class LeadTool {

    private static final String URL = "https://pawarpan.app.n8n.cloud/webhook/getmessage";

    @Tool(name = "ProcessLead", description = "Processes a lead by sending the contact number to an external service.")
    public String processLead(String contactNumber) {
        log.info("Process request for contact number: {}", contactNumber);
        OkHttpClient client = new OkHttpClient().newBuilder().build();
        MediaType mediaType = MediaType.parse("application/json");
        LeadProcessRequest leadProcessRequest = new LeadProcessRequest(contactNumber);
        Gson gson = new Gson();
        RequestBody body = RequestBody.create(gson.toJson(leadProcessRequest), mediaType);
        log.info("Sending request to URL: {}, with request body: {}", URL, leadProcessRequest);
        Request request = new Request.Builder()
                .url(URL)
                .method("POST", body)
                .addHeader("Content-Type", "application/json")
                .build();
        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful() && response.body() != null) {
                String responseBody = response.body().string();
                log.info("Lead processing response for contact number {}: {}", contactNumber, responseBody);
                return responseBody;
            } else {
                log.error("Failed to process lead for contact number {}: {}", contactNumber, response.message());
            }
        } catch (Exception e) {
            log.error("Error processing lead for contact number {}: {}", contactNumber, e.getMessage());
        } finally {
            log.info("Lead processing request completed for contact number: {}", contactNumber);
        }
        return "Failed to start onboarding process";
    }
}
