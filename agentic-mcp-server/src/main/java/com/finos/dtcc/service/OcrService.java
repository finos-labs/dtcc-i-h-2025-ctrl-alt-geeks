package com.finos.dtcc.service;

import com.finos.dtcc.entity.KycDetails;
import com.google.gson.Gson;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Slf4j
@Service
public class OcrService {

    public static final String URL = "http://18.226.222.162:8000/ocr-service/process/";

    public Optional<KycDetails> process(String clientId) {
        log.info("KYC document processing for client: {}", clientId);
        OkHttpClient client = new OkHttpClient();
        String url = URL + clientId;
        log.info("Requesting OCR processing at URL: {}", url);
        Request request = new Request.Builder().url(url).build();
        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful() || response.body() != null) {
                String json = response.body().string();
                log.info("OCR response for client {}: {}", clientId, json);
                Gson gson = new Gson();
                KycDetails kycDetails = gson.fromJson(json, KycDetails.class);
                return Optional.of(kycDetails);
            } else {
                log.error("Failed to process OCR for client {}: {}", clientId, response.message());
                return Optional.empty();
            }
        } catch (Exception e) {
            log.error("Error processing image: {}", e.getMessage());
            return Optional.empty();
        }
    }

}
