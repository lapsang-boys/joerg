import { Component, OnInit, Input } from '@angular/core';
import { Card } from '../card.type';
import { transition, useAnimation, trigger } from '@angular/animations';
import { fadeIn } from '../animations';
import { Observable, BehaviorSubject } from 'rxjs';

@Component({
	selector: 'app-card',
	templateUrl: './card.component.html',
	styleUrls: ['./card.component.css'],
	animations: [
		trigger('cardAnimation', [
			transition(
				':enter',
				useAnimation(fadeIn, {
					params: {
						time: '650ms ease-in-out',
						from: 0,
						to: 1
					}
				})
			)
		])
	]
})
export class CardComponent implements OnInit {

	@Input() card: Card;
	hovered = false;
	hoveredSubject: BehaviorSubject<boolean> = new BehaviorSubject(this.hovered);
	faceup = true;

	constructor() { }

	ngOnInit(): void {
		// setInterval(() => this.setFacing(), 2000);
	}

	handleHovered(hovered: boolean) {
		this.hovered = hovered;
		this.hoveredSubject.next(this.hovered);
	}

	setFacing() {
		this.faceup = Math.random() * 100 < 50 ? true : false;
	}
}
