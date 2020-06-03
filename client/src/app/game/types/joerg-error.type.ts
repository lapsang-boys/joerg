import { FromJson } from 'src/app/network/from.json';

export class JoergError implements FromJson {
	message: string;

	fromJson(json: Object) {
		console.log("JoergError", json);
		this.message = json['payload'];
	}
} 
