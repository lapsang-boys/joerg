import { Card } from "../card/card.type";

export class Cube {
	name: string;
	cards: Card[];

	constructor(name: string) {
		this.name = name;
		this.cards = [];
	}
}
