export interface Suggestion {
  id: number;
  text: string;
  tag: string;
}

export interface Item {
  id: number;
  quantity: number;
  listId: number;
  done: boolean;
  text: string;
}

export interface List {
  id:number;
  name:string;
  tags:string[];
  creation_date:string;
}
