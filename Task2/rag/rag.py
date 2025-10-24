import  psycopg2
import re
import json
from .generative_rag import gen_ans, Rag2Input
class PhoneRAGAgent:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
        self.cur = self.conn.cursor()
        print("RAG Agent connected to PostgreSQL.")

    def _extract_models(self, question):
        """Extract specific model names from the question."""
        question = question.lower()

        # Common patterns for Samsung model names
        patterns = [
            r's\d+(\s+)?(?:ultra|plus|\+)?',  # S22, S22 Ultra, S22+
            r'z\s*(?:fold|flip)\d+',  # Z Fold4, Z Flip4
            r'a\d+[es]?',  # A54, A54s
            r'note\s*\d+',  # Note 20
            r'galaxy\s+[a-z]+\s*\d+',  # Galaxy S22, Galaxy A54
        ]


        models_found = []

        for pattern in patterns:
            matches = re.finditer(pattern, question)
            for match in matches:
                model = match.group().strip()
                # Standardize model names
                model = model.replace('+', ' plus')
                model = ' '.join(word.capitalize() for word in model.split())
                models_found.append(model)

        return models_found

    def _extract_budget(self, question):
        """Extract budget if mentioned in the question."""
        question = question.lower()
        # Patterns like "under 500", "below 1000", "up to 800", "between 500 and 1000"
        between_match = re.search(r'between\s*(\d+)\s*(?:and|-)\s*(\d+)', question)
        under_match = re.search(r'(?:under|below|within|up to)\s*(\d+)', question)
        above_match = re.search(r'(?:above|over)\s*(\d+)', question)
        price_match = re.search(r'(?:price|budget)\s*(\d+)', question)

        if between_match:
            return int(between_match.group(1)), int(between_match.group(2))
        elif under_match:
            return 0, int(under_match.group(1))
        elif price_match:
            return 0, int(price_match.group(1))
        elif above_match:
            return int(above_match.group(1)),int(above_match.group(1))*2
        else:
            return None

    def _build_query(self, models=None, budget=None):
        """Build SQL query based on models and optional budget."""
        query = "SELECT * FROM phones"
        conditions = []
        params = []

        if models:
            like_conditions = ["LOWER(model_name) LIKE LOWER(%s)" for _ in models]
            conditions.append("(" + " OR ".join(like_conditions) + ")")
            params.extend([f"%{model}%" for model in models])

        if budget:
            min_price, max_price = budget
            conditions.append("price >= %s AND price <= %s")
            params.extend([min_price, max_price])

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        return query, params

    def _format_response(self, data, columns):
        if not data:
            return "I couldn't find any phones matching your query."
        # Format as individual phone listings
        response = []
        for row in data:
            phone_info = []
            for i, value in enumerate(row[1:], start=1):
                if value and value != "Not found":
                    field_name = columns[i]
                    phone_info.append(f"{field_name}: {value}")

            response.append("\n".join(phone_info))

        return response

    def answer_question(self, question):
        try:
            # 1. Extract models and budget
            models = self._extract_models(question)
            budget = self._extract_budget(question)

            # 2. Build and execute query
            query, params = self._build_query(models=models, budget=budget)
            self.cur.execute(query, params)

            # 3. Fetch results
            columns = [desc[0] for desc in self.cur.description]
            results = self.cur.fetchall()

            # 4. Format response
            response = self._format_response(results, columns)
            print(len(response))
            if results != []:
                response_dict = {"results": response}  # wrap list in a dict

                # Create the Rag2Input object
                question_to_gen = Rag2Input(data=response_dict, question=question)

                # Call gen_ans with the Rag2Input object
                generative_ans = gen_ans(question_to_gen)

                return generative_ans
            else:
                return response
        except Exception as e:
            return f"Sorry Encountered an error: {str(e)}"

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
            print("RAG Agent disconnected from PostgreSQL.")