package org.vicomtech.nlp.hackathon.database.restaurants;

import java.util.List;

import org.vicomtech.nlp.hackathon.model.Restaurant;

public interface RestaurantsRepositoryCustom {

	public List<Restaurant>findByCriteria(String municipality);
	
}
