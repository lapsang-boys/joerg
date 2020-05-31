import { Component, OnInit, Input } from '@angular/core';
import { Player } from '../../types/player.type';

@Component({
	selector: 'app-player-hand',
	templateUrl: './player-hand.component.html',
	styleUrls: ['./player-hand.component.css']
})
export class PlayerHandComponent implements OnInit {
	@Input() player: Player;
	@Input() renderSize: number;

	constructor() { }

	ngOnInit(): void {
	}

}
