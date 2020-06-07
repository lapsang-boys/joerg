import { Component, OnInit } from '@angular/core';
// Temp import, remove when server is up and running.
import { Card } from 'src/app/card/card.type';
import cards from 'src/app/library/cards.json';
import { CubeService } from "../cube.service";

@Component({
	selector: 'app-cube-library',
	templateUrl: './cube-library.component.html',
	styleUrls: ['./cube-library.component.css']
})
export class CubeLibraryComponent implements OnInit {
	cards: Card[] = [];

	constructor(
	  private cubeService: CubeService,
	) { }

	ngOnInit(): void {
		const cardArray = cards['cards'] as object[];
		for (const card of cardArray) {
			this.cards.push(new Card(card));
		}
	}

	add(card: Card): void {
	  this.cubeService.add(card);
	}
}
