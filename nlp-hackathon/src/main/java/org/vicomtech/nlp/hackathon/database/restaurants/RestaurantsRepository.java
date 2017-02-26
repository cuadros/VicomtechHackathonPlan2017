package org.vicomtech.nlp.hackathon.database.restaurants;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.vicomtech.nlp.hackathon.model.Restaurant;

public interface RestaurantsRepository extends RestaurantsRepositoryCustom,MongoRepository<Restaurant, String>{

}
