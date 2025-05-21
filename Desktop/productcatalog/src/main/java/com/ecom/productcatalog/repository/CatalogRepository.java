package com.ecom.productcatalog.repository;

import com.ecom.productcatalog.models.CatalogModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CatalogRepository extends JpaRepository<CatalogModel, Long> {
}
