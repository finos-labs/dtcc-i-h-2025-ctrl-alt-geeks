package com.finos.dtcc.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.*;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "LEAD")
public class Lead {

    @Id
    @Column(name = "lead_id", nullable = false)
    private Integer id;

    @Column(name = "lead_first_name")
    private String firstName;

    @Column(name = "lead_last_name")
    private String lastName;

    @Column(name = "lead_company_name")
    private String company;

    @Column(name = "lead_official_title")
    private String title;

    @Column(name = "lead_type")
    private String type;

    @Column(name = "lead_generation_source")
    private String source;

    @Column(name = "lead_status")
    private String status;

    @Column(name = "lead_contact_number")
    private String contactNumber;
}
