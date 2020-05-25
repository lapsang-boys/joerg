export class CardType {
	name: string;
	power: number;
	ruling: string;
	flavor: string;
	imgSrc: string;
	legendary: boolean;

	static fromJson(json: CardType): CardType {
		const card = new CardType();
		card.name = json.name;
		card.power = json.power;
		card.ruling = json.ruling;
		card.flavor = json.flavor;
		card.imgSrc = json.imgSrc;
		card.legendary = json.legendary;
		return card;
	}
}
