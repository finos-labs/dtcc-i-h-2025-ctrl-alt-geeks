package com.finos.dtcc.repository;

import com.finos.dtcc.entity.Lead;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface LeadRepository extends JpaRepository<Lead, Integer> {

    Optional<Lead> findFirstByContactNumber(String contactNumber);

    List<Lead> findAllByStatus(String status);
}
