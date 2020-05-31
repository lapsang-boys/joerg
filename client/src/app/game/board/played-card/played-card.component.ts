import { Component, OnInit, Input } from '@angular/core';
import { PlayedCard, PlayOrder } from '../../types/played.card.type';
import { GameService } from '../../game.service';
import { Board } from '../../types/board.type';

@Component({
	selector: 'app-played-card',
	templateUrl: './played-card.component.html',
	styleUrls: ['./played-card.component.css']
})
export class PlayedCardComponent implements OnInit {

	@Input() playedCard: PlayedCard;
	board: Board;
	pole: boolean;
	roundWinner: boolean;

	constructor(private game: GameService) { }

	ngOnInit(): void {
		this.game.getObservableBoard().subscribe(board =>{
			this.board = board;
			this.pole = this.isPole();
		})
	}

	getOrderClass() {
		return PlayOrder[this.playedCard.order];
	}

	isPole(): boolean {
		const poleIndex = this.board.pole;
		const playerIndex = this.playedCard.player.index;
		return poleIndex === playerIndex;
	}
}
