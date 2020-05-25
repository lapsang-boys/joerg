import { Component, OnInit, Input } from '@angular/core';
import { CardType } from '../card.type';

@Component({
	selector: 'app-card-front',
	templateUrl: './card-front.component.html',
	styleUrls: ['./card-front.component.css']
})
export class CardFrontComponent implements OnInit {

	@Input() card: CardType;

	constructor() { }

	ngOnInit(): void {
	}

}
