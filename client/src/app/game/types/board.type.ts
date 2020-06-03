import { Card } from "src/app/card/card.type";
import { Player } from './player.type';
import { FromJson } from 'src/app/network/from.json';
import { PlayedCard } from './played.card.type';

export class Board implements FromJson {
	boardId: number;
	blockedCards: Card[];
	cube: Card[];
	deck: Card[];
	graveyard: Map<Player, Card[]>;
	playedCards: PlayedCard[];
	playerStates: object;
	players: Player[];
	pole: Player;
	roundWinner: number;
	roundWinningCard: Card;
	startingHandSize: number;
	victories: Map<Player, number>;
	winsNeeded: number;

	constructor(boardId: number) {
		this.boardId = boardId;
	}

	fromJson(json: Object) {
		console.log("board", json);
		this.deck = (json['deck'] as object[]).map(raw => new Card(raw));
		this.cube = (json['cube']['cards'] as object[]).map(raw => new Card(raw));
		this.playedCards = (json['playedCards'] as object[]).map(raw => new PlayedCard(raw));
		this.players = (json['players'] as object[]).map((raw) => new Player(raw));
		this.pole = json['pole'];
		if (json['roundWinningCard']) {
			this.roundWinningCard = new Card(json['roundWinningCard']);
		}
	}
}
