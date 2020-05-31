import { Card } from "src/app/card/card.type";
import { Player } from './player.type';
import { FromJson } from 'src/app/network/from.json';
import { PlayedCard } from './played.card.type';

export class Board implements FromJson {
	board_id: number;
	blocked_cards: Card[];
	cube: Card[];
	deck: Card[];
	graveyard: Map<Player, Card[]>;
	played_cards: PlayedCard[];
	player_states: object;
	players: Player[];
	pole: number;
	round_winner: number;
	round_winning_card: Card;
	starting_hand_size: number;
	victories: Map<Player, number>;
	wins_needed: number;

	constructor(board_id: number) {
		this.board_id = board_id;
	}

	fromJson(json: Object) {
		console.log(json);
		this.deck = (json['deck'] as object[]).map(raw => new Card(raw));
		this.cube = (json['cube'] as object[]).map(raw => new Card(raw));
		this.played_cards = (json['played_cards'] as object[]).map(raw => new PlayedCard(raw));
		this.players = (json['players'] as object[]).map((raw) => new Player(raw));
		this.pole = json['pole'];
		if (json['round_winning_card']) {
			this.round_winning_card = new Card(json['round_winning_card']);
		}
	}
}
