package com.finos.dtcc.model.response;

public record FraudDetectionResponse(String customerId, boolean isFraud) {
}
