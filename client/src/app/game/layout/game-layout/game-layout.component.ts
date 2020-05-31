import { Component, OnInit } from '@angular/core';
import { GameService } from '../../game.service';
import { Player } from '../../types/player.type';

@Component({
	selector: 'app-game-layout',
	templateUrl: './game-layout.component.html',
	styleUrls: ['./game-layout.component.css']
})
export class GameLayoutComponent implements OnInit {
	playerSelf: Player;
	otherPlayers: Player[];

	constructor(private game: GameService) { }

	ngOnInit(): void {
		this.game.start();
		this.game.getObservableBoard().subscribe(board => {
			// Currently playing player is always players[0]
			this.playerSelf = board.players[0];
			this.otherPlayers = board.players.slice(1);
		});
	}

}
