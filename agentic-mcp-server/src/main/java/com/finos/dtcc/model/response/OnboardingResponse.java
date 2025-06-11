package com.finos.dtcc.model.response;

import com.finos.dtcc.enums.OnboardingStatus;

public record OnboardingResponse(
        String userId,
        OnboardingStatus onboardingStatus,
        String message) {
    public OnboardingResponse(String userId, OnboardingStatus onboardingStatus) {
        this(userId, onboardingStatus, "Onboarding process completed successfully.");
    }
}