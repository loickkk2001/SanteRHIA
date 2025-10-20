export interface Planning {
  _id?: string;
  user_id: string;
  date: string;
  activity_code: 'SOIN' | 'CONGÉ' | 'REPOS' | 'FORMATION' | 'ADMINISTRATIF';
  plage_horaire: string;
  created_at?: string;
  updated_at?: string;
  validated_by?: string;
  commentaire?: string;
  user_name?: string;
  user_matricule?: string;
}





