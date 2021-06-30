export class ProjectsService {
  
  projects = [
    {
      id: 0,
      title: "Coucou's Adventure",
      description: "Les aventures du poussin Coucou",
      image: {
        src: "https://images.unsplash.com/photo-1595707012809-0fdf633d5dca?ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8Y2hpY2t8ZW58MHx8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
        alt: "Poussin tout mignon"
      },
      lastUpdate: new Date()
    },
    {
      id: 1,
      title: "Projet 2",
      description: "Couscous party",
      image: {
        src: "https://images.unsplash.com/photo-1595707012809-0fdf633d5dca?ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8Y2hpY2t8ZW58MHx8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
        alt: "Poussin tout mignon"
      },
      lastUpdate: new Date()
    }
  ]

  constructor() {}


}