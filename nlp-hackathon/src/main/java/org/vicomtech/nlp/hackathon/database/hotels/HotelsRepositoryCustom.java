package org.vicomtech.nlp.hackathon.database.hotels;

import java.util.List;

import org.vicomtech.nlp.hackathon.model.Hotel;

public interface HotelsRepositoryCustom {

	public List<Hotel>findByCriteria(String municipality);
	
}
