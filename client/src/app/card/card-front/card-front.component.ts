import { Component, OnInit, Input } from '@angular/core';
import { Card } from '../card.type';
import { Observable } from 'rxjs';

@Component({
	selector: 'app-card-front',
	templateUrl: './card-front.component.html',
	styleUrls: ['./card-front.component.css']
})
export class CardFrontComponent implements OnInit {

	@Input() card: Card;
	@Input() hoveredObservable: Observable<boolean>;
	hovered: boolean = false;

	constructor() { }

	ngOnInit(): void {
		this.hoveredObservable.subscribe(hovered => this.hovered = hovered);
	}
}
