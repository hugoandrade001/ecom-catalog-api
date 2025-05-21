package com.ecom.productcatalog.repository;

import com.ecom.productcatalog.models.CatalogModel;
import com.ecom.productcatalog.models.ProductsModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProductRepository extends JpaRepository<ProductsModel, Long> {

    List<ProductsModel> findByCategory(CatalogModel category);
}
