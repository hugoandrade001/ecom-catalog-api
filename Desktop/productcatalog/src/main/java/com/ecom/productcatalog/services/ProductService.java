package com.ecom.productcatalog.services;

import com.ecom.productcatalog.models.CatalogModel;
import com.ecom.productcatalog.models.ProductsModel;
import com.ecom.productcatalog.repository.ProductRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;
@Service
public class ProductService {


    private ProductRepository productRepository;

    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    public List<ProductsModel> findAll() {
        return productRepository.findAll();
    }

    public List<ProductsModel> findByCategory(CatalogModel categoryId) {
        return productRepository.findByCategory(categoryId);
    }
}
