import { Component, OnInit, Input } from '@angular/core';
import { Card } from "../card.type";

@Component({
  selector: 'app-card-compact',
  templateUrl: './card-compact.component.html',
  styleUrls: ['./card-compact.component.css']
})
export class CardCompactComponent implements OnInit {
  @Input() card: Card;

  constructor() { }

  ngOnInit(): void {
  }

}
