import { Component, OnInit, Input } from '@angular/core';
import { Card } from '../card.type';

@Component({
	selector: 'app-card-front',
	templateUrl: './card-front.component.html',
	styleUrls: ['./card-front.component.css']
})
export class CardFrontComponent implements OnInit {

	@Input() card: Card;
	hovered: boolean = false;

	constructor() { }

	ngOnInit(): void {
	}

	handleHovered(hovered: boolean) {
		this.hovered = hovered;
	}
}
