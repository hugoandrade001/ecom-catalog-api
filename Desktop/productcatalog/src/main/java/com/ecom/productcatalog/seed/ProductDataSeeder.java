package com.ecom.productcatalog.seed;

import com.ecom.productcatalog.models.CatalogModel;
import com.ecom.productcatalog.models.ProductsModel;
import com.ecom.productcatalog.repository.CatalogRepository;
import com.ecom.productcatalog.repository.ProductRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class ProductDataSeeder implements CommandLineRunner {

    private final ProductRepository productRepository;
    private final CatalogRepository catalogRepository;

    public ProductDataSeeder(ProductRepository productRepository, CatalogRepository catalogRepository) {
        this.productRepository = productRepository;
        this.catalogRepository = catalogRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        if (productRepository.count() == 0) {
            CatalogModel category = catalogRepository.findAll().get(0); // pega a primeira categoria

            ProductsModel p1 = new ProductsModel();
            p1.setName("Produto 1");
            p1.setDescription("Descrição do Produto 1");
            p1.setImageUrl("https://imagem1.com");
            p1.setPrice(99.99);
            p1.setCategory(category);

            ProductsModel p2 = new ProductsModel();
            p2.setName("Produto 2");
            p2.setDescription("Descrição do Produto 2");
            p2.setImageUrl("https://imagem2.com");
            p2.setPrice(199.99);
            p2.setCategory(category);

            productRepository.save(p1);
            productRepository.save(p2);

            System.out.println("✅ Produtos adicionados com sucesso!");
        }
    }
}
