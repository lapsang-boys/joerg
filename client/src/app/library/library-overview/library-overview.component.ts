import { Component, OnInit } from '@angular/core';
// Temp import, remove when server is up and running.
import cards from '../cards.json';
import { CardType } from 'src/app/card/card.type';

@Component({
	selector: 'app-library-overview',
	templateUrl: './library-overview.component.html',
	styleUrls: ['./library-overview.component.css']
})
export class LibraryOverviewComponent implements OnInit {
	cards: CardType[] = [];

	constructor() { }

	ngOnInit(): void {
		const cardArray = cards['cards'] as CardType[];
		for (const card of cardArray) {
			this.cards.push(CardType.fromJson(card));
		}
	}

}
