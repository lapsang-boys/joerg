import { Card } from "src/app/card/card.type";
import { Player } from './player.type';
import { FromJson } from 'src/app/network/from.json';

export class Board implements FromJson {
	blocked_cards: Card[];
	cube: Card[];
	deck: Card[];
	graveyard: Map<Player, Card[]>;
	played_cards: Card[];
	player_states: object;
	players: Player[];
	pole: number;
	round_winner: number;
	round_winning_card: Card;
	starting_hand_size: number;
	victories: Map<Player, number>;
	wins_needed: number;

	constructor() {
	}

	fromJson(json: Object) {
		this.deck = (json['deck'] as object[]).map(raw => new Card(raw));
		this.cube = (json['cube'] as object[]).map(raw => new Card(raw));
		this.played_cards = (json['played_cards'] as object[]).map(raw => new Card(raw));
		this.players = (json['players'] as object[]).map((raw, index) => new Player(raw, index));
		this.pole = json['pole'];

		console.log(this);
	}
}
