import { Component, OnInit, Input } from '@angular/core';
import { Player } from '../../types/player.type';

@Component({
	selector: 'app-other-hands-container',
	templateUrl: './other-hands-container.component.html',
	styleUrls: ['./other-hands-container.component.css']
})
export class OtherHandsContainerComponent implements OnInit {

	@Input() players: Player[];

	constructor() { }

	ngOnInit(): void {
	}

}
