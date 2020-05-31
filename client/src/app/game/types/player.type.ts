import { Hand } from './hand.type';

export class Player {
	name: string;
	id: number;
	index: number;
	hand: Hand;

	PLAYERS = ['Pineapple', 'Lemon', 'Apple', 'Orange', 'Peach'];

	constructor(payload: object) {
		this.index = payload['num'];
		this.name = this.PLAYERS[this.index];
		this.id = this.index;
		this.hand = new Hand(payload);
	}
}
