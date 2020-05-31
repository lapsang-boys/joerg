import { Player } from './player.type';
import { Card } from 'src/app/card/card.type';

export class PlayedCard {
	card: Card;
	order: string;
	player: Player;
	revealed: boolean;

	PLAYERS = ['Pineapple', 'Lemon', 'Apple', 'Orange', 'Peach'];

	constructor(json: object) {
		console.log('played card const', json)
		this.card = new Card(json['card']);
		this.order = PlayOrder[json['order'] as keyof PlayOrder];
		this.player = new Player(json['player']);
		this.revealed = json['revealed'];
	}
}

export enum PlayOrder {
	attack = 1,
	defense = 2
}
